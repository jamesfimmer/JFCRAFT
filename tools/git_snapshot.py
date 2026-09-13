"""Materialize exact committed bytes, without checkout newline conversion."""
from contextlib import contextmanager
from pathlib import Path
import subprocess
import tempfile
import zipfile


@contextmanager
def snapshot(repository, commit):
    with tempfile.TemporaryDirectory(prefix='jfcraft-snapshot-') as directory:
        root = Path(directory)
        archive = root / 'snapshot.zip'
        subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', '-C', str(repository), 'archive', '--format=zip',
                        '--output=' + str(archive), commit, 'download-files'], check=True)
        destination = root / 'files'
        with zipfile.ZipFile(archive) as source:
            for member in source.infolist():
                target = (destination / member.filename).resolve()
                if not target.is_relative_to(destination.resolve()):
                    raise ValueError('Unsafe Git archive member')
            source.extractall(destination)
        yield destination
