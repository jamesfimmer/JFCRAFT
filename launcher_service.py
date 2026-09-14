"""Application settings and Minecraft process lifecycle, independent of Tk."""
from contextlib import contextmanager
import hashlib
import logging
from http.client import IncompleteRead
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
import requests
from urllib3.exceptions import HTTPError as Urllib3HTTPError

from jfcraft_core import Installer, atomic_json, Cancelled, load_manifest

VERSION = '2.0.0-dev'


def data_dir():
    return Path(os.environ.get('JFCRAFT_HOME', str(Path(os.environ.get('APPDATA', Path.home())) / 'JFCRAFT')))


def resource_dir():
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))


def load_settings():
    defaults = {'username': 'Player', 'min_ram': 1024, 'max_ram': 4096, 'java': '', 'pack': '', 'sources': []}
    path = data_dir() / 'settings.json'
    if path.exists():
        defaults.update(json.loads(path.read_text(encoding='utf-8')))
    return defaults


def validate_settings(settings):
    if not re.fullmatch(r'[A-Za-z0-9_]{3,16}', settings['username']):
        raise ValueError('Ник: 3–16 латинских букв, цифр или знак подчёркивания')
    try:
        low, high = int(settings['min_ram']), int(settings['max_ram'])
    except (TypeError, ValueError):
        raise ValueError('Память нужно указать целым числом в МБ') from None
    if not 512 <= low <= high <= 65536:
        raise ValueError('Память: от 512 до 65536 МБ, минимум не больше максимума')
    return dict(settings, min_ram=low, max_ram=high)


@contextmanager
def profile_lock(root):
    root.mkdir(parents=True, exist_ok=True)
    stream = (root / '.jfcraft.lock').open('a+b')
    try:
        if os.fstat(stream.fileno()).st_size == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        stream.close()
        raise ValueError('Эта сборка уже открыта в другом окне JFCRAFT') from None
    try:
        yield
    finally:
        stream.close()


def remove_pack(pack_id):
    """Remove an installation by retaining it in a recoverable local backup."""
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', pack_id):
        raise ValueError('Некорректный ID сборки')
    instances = (data_dir() / 'instances').resolve()
    root = instances / pack_id
    if root.is_symlink() or root.resolve().parent != instances:
        raise ValueError('Недопустимый путь сборки')
    backup = data_dir() / 'removed-packs' / (pack_id + '-' + uuid.uuid4().hex)
    with profile_lock(root):
        children = [p for p in root.iterdir() if p.name != '.jfcraft.lock']
        if any(p.is_symlink() or not p.resolve().is_relative_to(root.resolve()) for p in children):
            raise ValueError('Папка содержит ссылки за пределы сборки')
        backup.mkdir(parents=True)
        moved = []
        try:
            for child in children:
                child.rename(backup / child.name)
                moved.append(child.name)
        except Exception:
            for name in reversed(moved):
                (backup / name).rename(root / name)
            raise
    return backup


def check_java(executable, required):
    executable = executable.strip() or shutil.which('java')
    if not executable:
        raise ValueError(f'Укажи путь к 64-битной Java {required} в настройках')
    result = subprocess.run([executable, '-XshowSettings:properties', '-version'], capture_output=True, text=True,
                            errors='replace', timeout=15, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    output = result.stdout + result.stderr
    match = re.search(r'version "(?:1\.)?(\d+)', output)
    if result.returncode or not match or int(match[1]) != required:
        raise ValueError(f'Для этой сборки нужна Java {required}. Выбери подходящий java.exe')
    if 'sun.arch.data.model = 64' not in output and '64-Bit' not in output:
        raise ValueError('Требуется 64-битная Java')
    return executable


def ensure_forge(pack, root, java, report, cancel, repair=False):
    import minecraft_launcher_lib as mc
    callback = {'setStatus': lambda message: (check_cancel(cancel), report(message))}
    marker = root / '.jfcraft-runtime.json'
    identity = {k: pack[k] for k in ('minecraft', 'forge', 'installed_version')}
    version_file = root / 'versions' / pack['installed_version'] / (pack['installed_version'] + '.json')
    if not repair and marker.exists() and json.loads(marker.read_text(encoding='utf-8')) == identity and version_file.exists():
        return
    report('Установка Minecraft и Forge…')
    version_file.parent.mkdir(parents=True, exist_ok=True)
    # 6.5 can extract the legacy install_profile directly, despite its conservative
    # supports_automatic_install helper. The 1.7.10 build needs the trailing suffix.
    for attempt in range(1, 4):
        check_cancel(cancel)
        try:
            mc.forge.install_forge_version(pack['forge'], str(root), callback=callback, java=java)
            break
        except (requests.RequestException, Urllib3HTTPError, IncompleteRead) as error:
            logging.warning('Сбой загрузки Minecraft/Forge, попытка %s/3', attempt, exc_info=True)
            check_cancel(cancel)
            if attempt == 3:
                report('Не удалось завершить загрузку Minecraft/Forge после трёх попыток. Нажми «Играть», чтобы повторить.')
                raise requests.ConnectionError('Загрузка Minecraft/Forge прервалась после трёх попыток') from error
            report(f'Соединение прервалось при загрузке Minecraft/Forge. Повторная попытка {attempt + 1}/3…')
            if cancel.wait(attempt):
                check_cancel(cancel)
    if not version_file.exists():
        # Legacy installers use a display name for the directory but a different
        # versionInfo.id inside the JSON. Normalize to the actual launch ID.
        for candidate in (root / 'versions').glob('*/*.json'):
            metadata = json.loads(candidate.read_text(encoding='utf-8'))
            if metadata.get('id') == pack['installed_version']:
                atomic_json(version_file, metadata)
                break
    if not version_file.exists():
        raise ValueError(f"Forge не создал профиль {pack['installed_version']}")
    atomic_json(marker, identity)


def check_cancel(cancel):
    if cancel.is_set():
        raise Cancelled('Операция отменена')


def run_pack(pack, settings, play, report, progress, cancel):
    import minecraft_launcher_lib as mc
    settings = validate_settings(settings)
    root = data_dir() / 'instances' / pack['id']
    with profile_lock(root):
        installer = Installer(root, report, progress, cancel)
        installer.recover()
        state = root / '.jfcraft-state.json'
        installed = load_manifest(state) if state.exists() else None
        if installed:
            if installed['id'] != pack['id']:
                raise ValueError('Сохранённое описание относится к другой сборке.')
        can_fallback = bool(play and installed and
            (root / 'versions' / installed['installed_version'] / (installed['installed_version'] + '.json')).is_file())
        check_cancel(cancel)
        try:
            pack = refresh_pack(pack, report, require_online=play)
            check_cancel(cancel)
            java = check_java(settings.get('java', ''), pack['java'])
            same_runtime = installed and all(pack[k] == installed[k] for k in ('minecraft', 'forge', 'installed_version'))
            if not (can_fallback and same_runtime):
                # Runtime installation cannot be rolled back like pack files.
                can_fallback = False
                ensure_forge(pack, root, java, report, cancel, repair=not play)
            installer.install(pack)
        except requests.RequestException:
            check_cancel(cancel)
            if not can_fallback:
                raise ValueError('Не удалось скачать необходимые файлы. Для первой установки или восстановления нужен интернет.') from None
            installer.recover()
            pack = installed
            java = check_java(settings.get('java', ''), pack['java'])
            report('Обновление недоступно. Запускается установленная версия ' + pack['version'])
        if play:
            installer.clean_extra_mods(pack)
        check_cancel(cancel)
        if not play:
            return
        offline_uuid = uuid.UUID(bytes=hashlib.md5(('OfflinePlayer:' + settings['username']).encode()).digest(), version=3)
        options = {'username': settings['username'], 'uuid': str(offline_uuid), 'token': '0',
                   'launcherName': 'JFCRAFT', 'launcherVersion': VERSION,
                   'executablePath': java, 'gameDirectory': str(root),
                   'jvmArguments': [f"-Xms{settings['min_ram']}M", f"-Xmx{settings['max_ram']}M"]}
        command = mc.command.get_minecraft_command(pack['installed_version'], str(root), options)
        log_dir = root / 'logs'
        log_dir.mkdir(exist_ok=True)
        report('Minecraft запущен. Журнал игры: ' + str(log_dir / 'jfcraft-game.log'))
        with (log_dir / 'jfcraft-game.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen(command, cwd=root, stdout=log, stderr=subprocess.STDOUT)
            code = process.wait()
        if code:
            raise RuntimeError(f'Minecraft завершился с кодом {code}. См. logs/jfcraft-game.log')
        report('Игра закрыта')


def refresh_pack(pack, report, require_online=False):
    """A mutable HTTPS manifest points to immutable, checksum-pinned assets."""
    cache = data_dir() / 'manifests' / (pack['id'] + '.json')
    if cache.exists():
        cached = load_manifest(cache)
        if cached['id'] == pack['id'] and not older_manifest(cached, pack):
            pack = cached
    source = pack.get('update_url')
    if not source:
        report('У этой сборки нет канала обновлений. Проверяется сохранённый выпуск.')
        return pack
    report('Проверка обновлений сборки…')
    try:
        latest = load_manifest(source)
    except requests.RequestException:
        if require_online:
            raise
        report('Канал обновлений недоступен. Используется сохранённое описание сборки.')
        return pack
    if latest['id'] != pack['id']:
        raise ValueError('Канал обновлений вернул другую сборку')
    if older_manifest(latest, pack):
        report('На сервере прежняя редакция описания; используется исправленная локальная.')
        return pack
    # Keep the subscribed channel even when a release manifest omits it.
    latest['update_url'] = source
    if latest != pack:
        report(f"Доступен выпуск {latest['version']}. Будут проверены изменения.")
    else:
        report(f"Актуальный выпуск: {latest['version']}")
    atomic_json(cache, latest)
    return latest


def older_manifest(candidate, current):
    return (candidate['version'] == current['version'] and
            candidate.get('manifest_revision', 0) < current.get('manifest_revision', 0))


def sync_catalog(report):
    """Refresh the official library on an explicit install/update action only."""
    url = 'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/packs/catalog/index.json'
    response = requests.get(url, timeout=(10, 30))
    response.raise_for_status()
    catalog = response.json()
    if catalog.get('schema') != 1 or not isinstance(catalog.get('packs'), list) or len(catalog['packs']) > 100:
        raise ValueError('Некорректный каталог сборок')
    packs = []
    for pack_id in catalog['packs']:
        if not isinstance(pack_id, str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', pack_id):
            raise ValueError('Некорректное имя сборки в каталоге')
        source = f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/packs/{pack_id}.json'
        pack = load_manifest(source)
        if pack['id'] != pack_id:
            raise ValueError('Каталог вернул другую сборку')
        pack['update_url'] = source
        bundled = resource_dir() / 'packs' / (pack_id + '.json')
        if bundled.exists():
            local = load_manifest(bundled)
            if older_manifest(pack, local):
                pack = local
        packs.append(pack)
    for pack in packs:
        atomic_json(data_dir() / 'manifests' / (pack['id'] + '.json'), pack)
    report('Библиотека сборок обновлена с GitHub.')
    return packs
