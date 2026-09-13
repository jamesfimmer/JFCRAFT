"""Build Winter Craft and classic LOTR from a checked out, immutable Git snapshot."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jfcraft_core import atomic_json, sha256, safe_path, validate_manifest
from jfcraft_archives import archive_member, rar_members

COMMIT = 'c2150b27970dc4aed04ea7a99b9964c78d6485a2'
PACKS = [
    ('wintercraft', 'Winter Craft', 'WinterCraft-1.20.1', '1.20.1', '1.20.1-47.3.0', '1.20.1-forge-47.3.0', 17),
    ('middle-earth-classic', 'Middle-earth Chronicles Classic', 'Middle-Earth-Chronicles-1.7.10', '1.7.10',
     '1.7.10-10.13.4.1614-1.7.10', '1.7.10-Forge10.13.4.1614-1.7.10', 8),
]


def main(repository):
    repository = Path(repository).resolve()
    git = ['git', '-c', f'safe.directory={repository.as_posix()}', '-C', str(repository)]
    if subprocess.check_output(git + ['rev-parse', 'HEAD'], text=True).strip() != COMMIT:
        raise ValueError('Исходная копия должна соответствовать закреплённому коммиту')
    for pack_id, name, folder, minecraft, forge, installed, java in PACKS:
        root = repository / 'download-files' / folder
        listed = {line.strip() for line in (root / 'mod_list.txt').read_text(encoding='utf-8-sig').splitlines() if line.strip()}
        for name_in_list in listed:
            if not safe_path(root / 'mods', name_in_list).is_file():
                raise ValueError(f'Нет файла из mod_list: {name_in_list}')
        entries = {}
        base = f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/{COMMIT}/download-files/{folder}/'
        for source in sorted(root.rglob('*')):
            if not source.is_file():
                continue
            relative = source.relative_to(root).as_posix()
            if relative.startswith('mods/'):
                # The historical list selects the active version; nested loader
                # libraries are required too. Do not install obsolete jars.
                if relative.count('/') == 1 and source.name not in listed:
                    continue
                if source.suffix.lower() != '.jar':
                    continue
            elif not relative.startswith(('config/', 'shaderpacks/', 'resourcepacks/')) and relative not in {'options.txt', 'servers.dat'}:
                continue
            entries[relative] = dict(path=relative, size=source.stat().st_size, sha256=sha256(source),
                url=base + quote(relative, safe='/'), policy='preserve' if relative in {'options.txt', 'servers.dat'} else 'merge' if relative.startswith('config/') else 'managed')
        for archive_path in sorted(root.glob('*.rar')):
            top = archive_path.stem
            if top not in {'config', 'shaderpacks', 'resourcepacks'}:
                continue
            digest = sha256(archive_path)
            for member in rar_members(archive_path):
                safe_path(root, member)
                relative = member if member.startswith(top + '/') else top + '/' + member
                if relative in entries:
                    continue
                with archive_member(archive_path, member, 'rar') as stream:
                    size, checksum = 0, hashlib.sha256()
                    while chunk := stream.read(1024 * 1024):
                        size += len(chunk)
                        checksum.update(chunk)
                url = base + quote(archive_path.name)
                entries[relative] = dict(path=relative, size=size, sha256=checksum.hexdigest(), url=url,
                    policy='merge' if top == 'config' else 'managed', archive=dict(format='rar', member=member,
                    url=url, size=archive_path.stat().st_size, sha256=digest))
        manifest = dict(schema=1, id=pack_id, name=name, version='legacy-' + COMMIT[:8], minecraft=minecraft,
                        forge=forge, installed_version=installed, java=java, files=list(entries.values()),
                        update_url=f'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/packs/{pack_id}.json')
        validate_manifest(manifest)
        destination = Path(__file__).resolve().parents[1] / 'packs' / (pack_id + '.json')
        atomic_json(destination, manifest)
        print(f'{name}: {len(entries)} files, {len(listed)} listed mods', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository')
    main(parser.parse_args().repository)
