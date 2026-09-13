"""Pack manifests, verified downloads and recoverable installation."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import threading
from urllib.parse import urlsplit
import uuid
import zipfile
import requests
from jfcraft_archives import archive_member


class Cancelled(Exception):
    pass


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    with temp.open('w', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(root, name):
    root = Path(root)
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Недопустимый путь файла')
    parts = name.split('/')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *[f'COM{i}' for i in range(10)], *[f'LPT{i}' for i in range(10)]}
    if any(p in ('', '.', '..') or p.endswith(('.', ' ')) or p.split('.')[0].upper() in reserved
           or any(c in p for c in '<>"|?*') or any(ord(c) < 32 for c in p) for p in parts):
        raise ValueError(f'Недопустимый путь: {name}')
    target = root.joinpath(*parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Путь выходит за каталог сборки: {name}')
    return target


def https_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Необходим HTTPS URL без пароля')
    return value


def validate_manifest(data):
    if not isinstance(data, dict):
        raise ValueError('Описание сборки должно быть объектом JSON')
    if 'update_url' in data:
        https_url(data['update_url'])
    if data.get('schema') != 1 or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', data.get('id', '')):
        raise ValueError('Некорректный формат описания сборки')
    for key in ('name', 'version', 'minecraft', 'forge', 'installed_version'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'Не задано поле {key}')
    if type(data.get('java')) is not int or data['java'] < 8:
        raise ValueError('Не задана версия Java')
    if not data['forge'].startswith(data['minecraft'] + '-'):
        raise ValueError('Forge не соответствует Minecraft')
    for key in ('minecraft', 'forge', 'installed_version'):
        safe_path(Path.cwd(), data[key])
        if '/' in data[key]:
            raise ValueError('Версия не может содержать путь')
    if not isinstance(data.get('files'), list):
        raise ValueError('Не задан список файлов')
    seen = set()
    for item in data['files']:
        name = item['path']
        safe_path(Path.cwd(), name)
        if name.split('/')[0] not in {'mods', 'config', 'defaultconfigs', 'resourcepacks', 'shaderpacks', 'scripts', 'kubejs'} and name not in {'options.txt', 'servers.dat'}:
            raise ValueError(f'Файл вне разрешённых каталогов: {name}')
        if name.casefold() in seen or any(name.casefold().startswith(p + '/') or p.startswith(name.casefold() + '/') for p in seen):
            raise ValueError(f'Конфликт путей: {name}')
        seen.add(name.casefold())
        if not re.fullmatch(r'[a-f0-9]{64}', item.get('sha256', '')) or type(item.get('size')) is not int or item['size'] < 0:
            raise ValueError(f'Нет контрольной суммы или размера: {name}')
        https_url(item['url'])
        if 'archive' in item:
            archive = item['archive']
            https_url(archive['url'])
            if not re.fullmatch(r'[a-f0-9]{64}', archive.get('sha256', '')) or type(archive.get('size')) is not int or archive['size'] < 0:
                raise ValueError('Некорректный архив')
            safe_path(Path.cwd(), archive['member'])
            if archive.get('format', 'zip') not in {'zip', 'rar'}:
                raise ValueError('Неизвестный формат архива')
        if item.get('policy', 'managed') not in {'managed', 'preserve', 'merge'}:
            raise ValueError(f'Неизвестная политика файла: {name}')
    return data


def load_manifest(source):
    if str(source).startswith('https://'):
        with requests.get(https_url(source), timeout=(10, 30), stream=True) as response:
            response.raise_for_status()
            https_url(response.url)
            content = bytearray()
            for chunk in response.iter_content(65536):
                content.extend(chunk)
                if len(content) > 8 * 1024 * 1024:
                    raise ValueError('Описание сборки слишком большое')
            data = json.loads(content)
    else:
        data = json.loads(Path(source).read_text(encoding='utf-8'))
    return validate_manifest(data)


class Installer:
    def __init__(self, root, report=lambda message: None, progress=lambda value, total: None, cancel=None):
        self.root = Path(root)
        self.report = report
        self.progress = progress
        self.cancel = cancel or threading.Event()

    def check_cancel(self):
        if self.cancel.is_set():
            raise Cancelled('Операция отменена')

    def download(self, item, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(3):
            self.check_cancel()
            try:
                with requests.get(item['url'], stream=True, timeout=(10, 30)) as response:
                    response.raise_for_status()
                    https_url(response.url)
                    digest, count = hashlib.sha256(), 0
                    with target.open('wb') as stream:
                        for chunk in response.iter_content(256 * 1024):
                            self.check_cancel()
                            count += len(chunk)
                            if count > item['size']:
                                raise ValueError('Размер загрузки превышает манифест')
                            stream.write(chunk)
                            digest.update(chunk)
                    if count != item['size'] or digest.hexdigest() != item['sha256']:
                        raise ValueError(f"Файл {item['path']} не соответствует описанию сборки: "
                                         f"ожидалось {item['size']} байт / {item['sha256']}, "
                                         f"получено {count} байт / {digest.hexdigest()}")
                return
            except (requests.RequestException, ValueError):
                if attempt == 2:
                    raise
                self.report(f"Повторная загрузка: {item['path']}")
                if self.cancel.wait(attempt + 1):
                    self.check_cancel()

    def recover(self):
        journal = self.root / '.jfcraft-journal.json'
        if not journal.exists():
            return
        data = json.loads(journal.read_text(encoding='utf-8'))
        backup = safe_path(self.root, data['backup'])
        for operation in reversed(data['operations']):
            target = safe_path(self.root, operation['path'])
            if operation['existed']:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(safe_path(backup, operation['path']), target)
            elif target.is_file():
                target.unlink()
        atomic_json(self.root / '.jfcraft-state.json', data['previous'])
        journal.unlink()
        self.report('Незавершённая установка восстановлена')

    def extra_mods(self, manifest):
        """Return files absent from the pack, including version subdirectories."""
        wanted = {item['path'].casefold() for item in manifest['files']}
        mods = safe_path(self.root, 'mods')
        if mods.is_symlink() or mods.resolve() != mods.absolute():
            raise ValueError('Папка mods не должна быть ссылкой на другую папку')
        extras = []
        for directory, directories, files in os.walk(mods, followlinks=False):
            self.check_cancel()
            for name in directories + files:
                path = Path(directory) / name
                relative = path.relative_to(self.root).as_posix()
                safe_path(self.root, relative)
                if path.is_symlink() or path.resolve() != path.absolute():
                    raise ValueError(f'Ссылка внутри папки mods не допускается: {relative}')
            for name in files:
                relative = (Path(directory) / name).relative_to(self.root).as_posix()
                if relative.casefold() not in wanted:
                    extras.append(relative)
        return extras

    def clean_extra_mods(self, manifest):
        """Local-only cleanup before launch, with recoverable backups."""
        validate_manifest(manifest)
        extras = self.extra_mods(manifest)
        if not extras:
            return
        backup = self.root / '.jfcraft-backups' / uuid.uuid4().hex
        for name in extras:
            self.check_cancel()
            saved = safe_path(backup, name)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(safe_path(self.root, name), saved)
        journal = self.root / '.jfcraft-journal.json'
        atomic_json(journal, {'backup': backup.relative_to(self.root).as_posix(),
                            'previous': manifest,
                            'operations': [{'path': name, 'existed': True} for name in extras]})
        try:
            for name in extras:
                self.check_cancel()
                safe_path(self.root, name).unlink()
            journal.unlink()
        except Exception:
            self.recover()
            raise
        for name in extras:
            self.report(f'Лишний файл убран из mods в резервную копию: {name}')

    def install(self, manifest):
        validate_manifest(manifest)
        self.root.mkdir(parents=True, exist_ok=True)
        self.recover()
        state_path = self.root / '.jfcraft-state.json'
        previous = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {'files': []}
        if previous.get('files'):
            validate_manifest(previous)
            if previous['id'] != manifest['id']:
                raise ValueError('В этой папке установлена другая сборка')
        transaction = uuid.uuid4().hex
        staging = self.root / '.jfcraft-staging' / transaction
        backup = self.root / '.jfcraft-backups' / transaction
        changes = []
        old_files = {item['path'].casefold(): item for item in previous['files']}
        try:
            for index, item in enumerate(manifest['files']):
                self.check_cancel()
                target = safe_path(self.root, item['path'])
                existing_hash = sha256(target) if target.is_file() else None
                keep_config = item.get('policy') == 'merge' and existing_hash is not None and existing_hash != old_files.get(item['path'].casefold(), {}).get('sha256')
                valid = target.is_file() and (item.get('policy') == 'preserve' or keep_config or (target.stat().st_size == item['size'] and existing_hash == item['sha256']))
                if keep_config and existing_hash != item['sha256']:
                    self.report(f"Сохранён пользовательский конфиг: {item['path']}")
                if not valid:
                    self.report(f"Загрузка: {item['path']}")
                    incoming = safe_path(staging, item['path'])
                    if 'archive' in item:
                        archive = item['archive']
                        cached = staging / '.archives' / archive['sha256']
                        if not cached.exists():
                            self.download(dict(archive, path=archive['member']), cached)
                        incoming.parent.mkdir(parents=True, exist_ok=True)
                        with archive_member(cached, archive['member'], archive.get('format', 'zip')) as source, incoming.open('wb') as output:
                            count = 0
                            while chunk := source.read(256 * 1024):
                                self.check_cancel()
                                count += len(chunk)
                                if count > item['size']:
                                    raise ValueError('Размер файла в архиве превышает манифест')
                                output.write(chunk)
                        if incoming.stat().st_size != item['size'] or sha256(incoming) != item['sha256']:
                            raise ValueError('Повреждён файл внутри архива')
                    else:
                        self.download(item, incoming)
                    changes.append(item['path'])
                self.progress(index + 1, len(manifest['files']))
            wanted = {item['path'].casefold() for item in manifest['files']}
            for old in previous['files']:
                if old['path'].casefold() not in wanted and old.get('policy', 'managed') == 'managed' and safe_path(self.root, old['path']).is_file():
                    changes.append(old['path'])
            for name in self.extra_mods(manifest):
                if name not in changes:
                    changes.append(name)
            self.check_cancel()
            operations = []
            for name in changes:
                target = safe_path(self.root, name)
                if target.exists() and not target.is_file():
                    raise ValueError(f'Ожидался файл: {name}')
                operations.append({'path': name, 'existed': target.exists()})
                if target.exists():
                    saved = safe_path(backup, name)
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(target, saved)
            journal = self.root / '.jfcraft-journal.json'
            atomic_json(journal, {'backup': backup.relative_to(self.root).as_posix(), 'operations': operations, 'previous': previous})
            try:
                for name in changes:
                    target, incoming = safe_path(self.root, name), safe_path(staging, name)
                    if incoming.exists():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        os.replace(incoming, target)
                    elif target.exists():
                        target.unlink()
                atomic_json(state_path, manifest)
                journal.unlink()
            except Exception:
                self.recover()
                raise
            self.report(f"Сборка {manifest['version']} проверена. Изменено файлов: {len(changes)}")
        finally:
            if staging.exists():
                shutil.rmtree(staging)
