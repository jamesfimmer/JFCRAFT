"""Find local Java or install a verified portable Temurin JRE."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid
import zipfile

import requests
from jfcraft_core import Cancelled, Installer, safe_path, https_url


def candidates(home, preferred=''):
    if preferred:
        yield preferred
    for path in sorted(Path(home).glob('java-*/installed-*/*/bin/java.exe'), reverse=True):
        yield str(path)
    for variable in ('JAVA_HOME', 'JDK_HOME'):
        if os.environ.get(variable):
            yield str(Path(os.environ[variable]) / 'bin/java.exe')
    if shutil.which('java'):
        yield shutil.which('java')
    base = Path(os.environ.get('ProgramFiles', 'C:/Program Files'))
    for vendor in ('Java', 'Eclipse Adoptium', 'Microsoft', 'Amazon Corretto', 'Zulu'):
        for path in (base / vendor).glob('*/bin/java.exe'):
            yield str(path)


def find_java(required, home, preferred, verify, cancel):
    seen = set()
    for candidate in candidates(home, preferred):
        if cancel.is_set():
            raise Cancelled('Операция отменена')
        if candidate in seen:
            continue
        seen.add(candidate)
        try:
            return verify(candidate, required)
        except (ValueError, OSError, subprocess.SubprocessError):
            pass
    return None


def install_java(required, home, verify, report, progress, cancel):
    if os.name != 'nt':
        raise ValueError('Автоустановка Java пока поддерживается только на Windows.')
    if cancel.is_set():
        raise Cancelled('Операция отменена')
    report(f'Скачивание Java {required} x64 (Eclipse Temurin)…')
    url = f'https://api.adoptium.net/v3/assets/latest/{required}/hotspot'
    with requests.get(url, params={'architecture': 'x64', 'image_type': 'jre',
                                  'os': 'windows', 'vendor': 'eclipse'}, timeout=(10, 30)) as response:
        response.raise_for_status()
        releases = response.json()
    if not releases:
        raise ValueError(f'Не найден выпуск Java {required} для Windows x64.')
    package = releases[0]['binary']['package']
    if not re.fullmatch('[a-f0-9]{64}', package['checksum']) or not 0 < package['size'] < 1024**3:
        raise ValueError('Некорректное описание дистрибутива Java.')
    https_url(package['link'])
    home = Path(home)
    home.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='staging-', dir=home) as temp:
        staging = Path(temp)
        archive = staging / 'java.zip'
        Installer(staging, report, progress, cancel).download(
            dict(path='java.zip', url=package['link'], size=package['size'], sha256=package['checksum']), archive)
        extracted = staging / 'runtime'
        report(f'Распаковка и проверка Java {required}…')
        with zipfile.ZipFile(archive) as bundle:
            members = bundle.infolist()
            if sum(item.file_size for item in members) > 2 * 1024**3:
                raise ValueError('Слишком большой архив Java.')
            for item in members:
                if cancel.is_set():
                    raise Cancelled('Операция отменена')
                target = safe_path(extracted, item.filename.rstrip('/'))
                if item.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(item) as src, target.open('wb') as dst:
                        while chunk := src.read(256 * 1024):
                            if cancel.is_set():
                                raise Cancelled('Операция отменена')
                            dst.write(chunk)
        executables = list(extracted.glob('*/bin/java.exe'))
        if len(executables) != 1:
            raise ValueError('В архиве не найден java.exe.')
        verify(str(executables[0]), required)
        if cancel.is_set():
            raise Cancelled('Операция отменена')
        destination = home / ('installed-' + uuid.uuid4().hex)
        relative = executables[0].relative_to(extracted)
        extracted.rename(destination)
    report(f'Java {required} установлена.')
    return str(destination / relative)
