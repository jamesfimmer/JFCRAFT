"""Read a single archive member; never extract an archive into the game folder."""
from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def tar_executable():
    executable = Path(os.environ.get('SystemRoot', 'C:/Windows')) / 'System32' / 'tar.exe' if os.name == 'nt' else shutil.which('bsdtar')
    if not executable or not Path(executable).is_file():
        raise ValueError('Для старых RAR-сборок нужен системный tar.exe из Windows 10/11')
    return str(executable)


def rar_members(path):
    result = subprocess.run([tar_executable(), '-tf', str(path)], capture_output=True, timeout=60,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), check=True)
    return [name for name in result.stdout.decode('utf-8').splitlines() if not name.endswith('/')]


@contextmanager
def archive_member(path, member, kind='zip'):
    if kind == 'zip':
        with zipfile.ZipFile(path) as archive, archive.open(member) as stream:
            yield stream
        return
    if kind != 'rar':
        raise ValueError('Неизвестный формат архива')
    # bsdtar interprets member operands as glob patterns, even without a shell.
    pattern = ''.join({'[': '[[]', '*': '[*]', '?': '[?]'}.get(c, c) for c in member)
    with tempfile.TemporaryFile() as errors:
        process = subprocess.Popen([tar_executable(), '-xOf', str(path), '--', pattern], stdout=subprocess.PIPE,
                                   stderr=errors, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        try:
            yield process.stdout
            if process.wait(timeout=30):
                raise ValueError(f'Не удалось прочитать файл из RAR: {member}')
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()
            process.stdout.close()
