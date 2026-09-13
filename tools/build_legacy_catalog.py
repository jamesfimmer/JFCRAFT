"""Reproduce manifests for the three historical, Git-hosted packs."""
import hashlib
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote
import zipfile
from contextlib import closing

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jfcraft_core import atomic_json, sha256, validate_manifest
from git_snapshot import snapshot
from jfcraft_archives import rar_members, archive_member

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


def build(source_root):
    tracked = set(subprocess.check_output(['git', '-c', f'safe.directory={ROOT.as_posix()}', 'ls-tree', '-r', '--name-only', COMMIT], cwd=ROOT, text=True).splitlines())
    for pack_id, name, folder, minecraft, forge in PACKS:
        manifest = dict(schema=1, id=pack_id, name=name, version='legacy-2024', minecraft=minecraft,
                        forge=f'{minecraft}-{forge}', installed_version=f'{minecraft}-forge-{forge}', java=17, files=[])
        manifest['update_url'] = f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/packs/{pack_id}.json'
        source = source_root / 'download-files' / folder
        archive_tops = {p.stem for p in source.glob('*.rar')} | {p.stem for p in source.glob('*.zip')}
        files = {}
        for file in sorted(source.rglob('*')):
            if not file.is_file() or file.relative_to(source_root).as_posix() not in tracked:
                continue
            relative = file.relative_to(source).as_posix()
            url = BASE + quote(file.relative_to(source_root).as_posix(), safe='/')
            if allowed(relative):
                if relative.split('/')[0] in archive_tops and relative.split('/')[0] in {'shaderpacks', 'resourcepacks', 'config'}:
                    continue
                files[relative] = record(relative, file.read_bytes(), url)
            elif relative in {'mods.zip', 'config.zip', 'options.zip', 'shaderpacks.zip', 'resourcepacks.zip', 'config.rar', 'shaderpacks.rar', 'resourcepacks.rar'}:
                digest = sha256(file)
                kind = file.suffix[1:]
                if kind == 'rar':
                    members = rar_members(file)
                else:
                    with zipfile.ZipFile(file) as archive:
                        members = [item.filename for item in archive.infolist() if not item.is_dir()]
                for member in members:
                        target = member
                        if kind == 'rar' and top in {'shaderpacks', 'resourcepacks'}:
                            if not member.lower().endswith('.zip'):
                                continue
                            target = top + '/' + Path(member).name
                        top = relative[:-4]
                        if top in ALLOWED and not target.startswith(top + '/'):
                            target = top + '/' + target
                        if not allowed(target):
                            continue
                        with archive_member(file, member, kind) as stream:
                            entry = record(target, stream.read(), url)
                        entry['archive'] = dict(url=url, size=file.stat().st_size, sha256=digest, member=member, format=kind)
                        files.setdefault(target, entry)
        manifest['files'] = list(files.values())
        manifest['manifest_revision'] = 2
        validate_manifest(manifest)
        atomic_json(ROOT / 'packs' / (pack_id + '.json'), manifest)
        print(name, len(files), 'files')


if __name__ == '__main__':
    with snapshot(ROOT, COMMIT) as source_root:
        build(source_root)
