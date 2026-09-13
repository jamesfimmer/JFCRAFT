"""Reproduce manifests for the three historical, Git-hosted packs."""
import hashlib
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jfcraft_core import atomic_json, sha256, validate_manifest

ROOT = Path(__file__).resolve().parents[1]
COMMIT = '262c645cacbe76de64b1bf5f3831a4c22d73e412'
BASE = f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/{COMMIT}/'
PACKS = [
    ('vanilla-expanded', 'Vanilla Expanded', 'VanillaExpanded-1.20.1', '1.20.1', '47.2.0'),
    ('pokecraft', 'Pokecraft', 'Pokecraft-1.20.1', '1.20.1', '47.3.0'),
    ('new-ic', 'New IC', 'NewIC-1.19.2', '1.19.2', '43.3.5'),
]
ALLOWED = {'mods', 'config', 'defaultconfigs', 'shaderpacks', 'resourcepacks', 'scripts'}


def allowed(name):
    return name.split('/')[0] in ALLOWED or name in {'options.txt', 'servers.dat'}


def record(name, content, url):
    return dict(path=name, size=len(content), sha256=hashlib.sha256(content).hexdigest(), url=url,
                policy='preserve' if name in {'options.txt', 'servers.dat'} else 'merge' if name.startswith('config/') else 'managed')


def main():
    tracked = set(subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'ls-tree', '-r', '--name-only', COMMIT], cwd=ROOT, text=True).splitlines())
    for pack_id, name, folder, minecraft, forge in PACKS:
        manifest = dict(schema=1, id=pack_id, name=name, version='legacy-2024', minecraft=minecraft,
                        forge=f'{minecraft}-{forge}', installed_version=f'{minecraft}-forge-{forge}', java=17, files=[])
        manifest['update_url'] = f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/packs/{pack_id}.json'
        source = ROOT / 'download-files' / folder
        files = {}
        for file in sorted(source.rglob('*')):
            if not file.is_file() or file.relative_to(ROOT).as_posix() not in tracked:
                continue
            relative = file.relative_to(source).as_posix()
            url = BASE + quote(file.relative_to(ROOT).as_posix(), safe='/')
            if allowed(relative):
                files[relative] = record(relative, file.read_bytes(), url)
            elif relative in {'mods.zip', 'config.zip', 'options.zip', 'shaderpacks.zip'}:
                digest = sha256(file)
                with zipfile.ZipFile(file) as archive:
                    for member in archive.infolist():
                        if member.is_dir():
                            continue
                        target = member.filename
                        top = relative[:-4]
                        if top in ALLOWED and not target.startswith(top + '/'):
                            target = top + '/' + target
                        if not allowed(target):
                            continue
                        entry = record(target, archive.read(member), url)
                        entry['archive'] = dict(url=url, size=file.stat().st_size, sha256=digest, member=member.filename)
                        files.setdefault(target, entry)
        manifest['files'] = list(files.values())
        validate_manifest(manifest)
        atomic_json(ROOT / 'packs' / (pack_id + '.json'), manifest)
        print(name, len(files), 'files')


if __name__ == '__main__':
    main()
