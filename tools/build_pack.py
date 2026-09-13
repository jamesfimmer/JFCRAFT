"""Create a manifest for files committed under download-files."""
import argparse
import hashlib
from pathlib import Path
import sys
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jfcraft_core import atomic_json, sha256, validate_manifest

DIRECTORIES = {'mods', 'config', 'defaultconfigs', 'resourcepacks', 'shaderpacks', 'scripts', 'kubejs'}


def build(source, output, pack_id, name, version, minecraft, forge, installed_version, java, repository, folder):
    source, output = Path(source).resolve(), Path(output).resolve()
    manifest = dict(schema=1, id=pack_id, name=name, version=version, minecraft=minecraft,
                    forge=forge, installed_version=installed_version, java=java, files=[])
    manifest['update_url'] = f'https://raw.githubusercontent.com/{repository}/main/packs/{pack_id}.json'
    validate_manifest(manifest)
    output.mkdir(parents=True, exist_ok=True)
    base = f'https://raw.githubusercontent.com/{repository}/main/download-files/{quote(folder, safe="")}/'
    for file in sorted(source.rglob('*')):
        if not file.is_file():
            continue
        relative = file.relative_to(source).as_posix()
        if relative.split('/')[0] not in DIRECTORIES and relative not in {'options.txt', 'servers.dat'}:
            continue
        if not file.resolve().is_relative_to(source):
            raise ValueError('Символическая ссылка за пределами сборки')
        digest = sha256(file)
        manifest['files'].append(dict(path=relative, size=file.stat().st_size, sha256=digest, url=base + quote(relative, safe='/'),
                                     policy='preserve' if relative in {'options.txt', 'servers.dat'} else 'merge' if relative.startswith('config/') else 'managed'))
    validate_manifest(manifest)
    atomic_json(output, manifest)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output', help='Путь packs/<id>.json')
    parser.add_argument('--folder', required=True, help='Имя папки внутри download-files')
    for field in ('id', 'name', 'version', 'minecraft', 'forge', 'installed-version'):
        parser.add_argument('--' + field, required=True)
    parser.add_argument('--java', type=int, required=True)
    parser.add_argument('--repository', default='jamesfimmer/JFCRAFT')
    args = parser.parse_args()
    result = build(args.source, args.output, args.id, args.name, args.version, args.minecraft, args.forge,
                   args.installed_version, args.java, args.repository, args.folder)
    print(f"Готово: {len(result['files'])} файлов. Манифест: {args.output}")
