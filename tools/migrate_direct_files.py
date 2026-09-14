"""One-time migration preserving the exact bytes described by existing manifests."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import uuid
from urllib.parse import unquote, urlsplit, quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from jfcraft_core import atomic_json, safe_path, sha256, validate_manifest
from jfcraft_archives import archive_member, rar_members, tar_executable


def main():
    workspace = ROOT / 'output' / ('direct-migration-' + uuid.uuid4().hex)
    workspace.mkdir(parents=True)
    plans = []
    assets = {}
    extracted = {}
    for manifest_path in sorted((ROOT / 'packs').glob('*.json')):
        pack = json.loads(manifest_path.read_text(encoding='utf-8'))
        if not any('archive' in item for item in pack['files']):
            # Direct-only packs still need files restored from their pinned snapshot.
            if all('/main/download-files/' in f['url'] for f in pack['files']):
                continue
        atomic_json(workspace / 'manifests' / manifest_path.name, pack)
        updated = dict(pack, files=[], manifest_revision=pack.get('manifest_revision', 0) + 1)
        folders = set()
        for item in pack['files']:
            asset = item.get('archive', item)
            url = asset['url']
            parts = unquote(urlsplit(url).path).split('/')
            commit, relative = parts[3], '/'.join(parts[4:])
            folder = relative.split('/')[1]
            folders.add(folder)
            if url not in assets:
                cached = workspace / 'sources' / hashlib.sha256(url.encode()).hexdigest()
                cached.parent.mkdir(exist_ok=True)
                with cached.open('wb') as stream:
                    subprocess.run(['git', 'show', f'{commit}:{relative}'], cwd=ROOT, stdout=stream, check=True)
                if cached.stat().st_size != asset['size'] or sha256(cached) != asset['sha256']:
                    raise ValueError('Source differs from manifest: ' + url)
                assets[url] = cached
            source = assets[url]
            staged = safe_path(workspace / 'staged' / folder, item['path'])
            staged.parent.mkdir(parents=True, exist_ok=True)
            if 'archive' in item:
                archive = item['archive']
                kind = archive.get('format', 'zip')
                if kind == 'rar' and item['path'].startswith('config/'):
                    if url not in extracted:
                        destination = workspace / 'extracted' / source.name
                        destination.mkdir(parents=True)
                        for member in rar_members(source):
                            safe_path(destination, member)
                        subprocess.run([tar_executable(), '-xf', str(source), '-C', str(destination)], check=True, timeout=180)
                        extracted[url] = destination
                    shutil.copyfile(safe_path(extracted[url], archive['member']), staged)
                else:
                    with archive_member(source, archive['member'], kind) as stream, staged.open('wb') as target:
                        shutil.copyfileobj(stream, target)
            else:
                shutil.copyfile(source, staged)
            if staged.stat().st_size != item['size'] or sha256(staged) != item['sha256']:
                raise ValueError('Extracted content differs: ' + item['path'])
            direct = {k: v for k, v in item.items() if k != 'archive'}
            direct['url'] = 'https://raw.githubusercontent.com/jamesfimmer/JFCRAFT/main/' + quote(f'download-files/{folder}/{item["path"]}', safe='/')
            updated['files'].append(direct)
        if len(folders) != 1:
            raise ValueError('Expected one source folder per pack')
        validate_manifest(updated)
        plans.append((manifest_path, folders.pop(), updated))
        print(f'Verified {pack["id"]}: {len(pack["files"])} exact files', flush=True)

    # Apply only after all packs have passed byte-for-byte validation.
    for manifest_path, folder, pack in plans:
        target_root = safe_path(ROOT / 'download-files', folder)
        for item in pack['files']:
            target = safe_path(target_root, item['path'])
            if target.exists() and sha256(target) != item['sha256']:
                saved = safe_path(workspace / 'previous-files' / folder, item['path'])
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, saved)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(safe_path(workspace / 'staged' / folder, item['path']), target)
        for wrapper in list(target_root.glob('*.zip')) + list(target_root.glob('*.rar')):
            if wrapper.stem not in {'mods', 'config', 'options', 'shaderpacks', 'resourcepacks'}:
                continue
            saved = workspace / 'previous-files' / folder / wrapper.name
            saved.parent.mkdir(parents=True, exist_ok=True)
            wrapper.rename(saved)
        atomic_json(manifest_path, pack)
    # Keep source folders equal to the installed manifest. Preserve unused old
    # versions and formerly ignored config files outside the published folders.
    leftovers = 0
    for manifest_path in sorted((ROOT / 'packs').glob('*.json')):
        pack = json.loads(manifest_path.read_text(encoding='utf-8'))
        folder = unquote(urlsplit(pack['files'][0]['url']).path).split('/')[5]
        target_root = safe_path(ROOT / 'download-files', folder)
        wanted = {f['path'].casefold() for f in pack['files']}
        for path in list(target_root.rglob('*')):
            if not path.is_file():
                continue
            relative = path.relative_to(target_root).as_posix()
            if relative.split('/')[0] not in {'mods', 'config', 'defaultconfigs', 'resourcepacks', 'shaderpacks', 'scripts', 'kubejs'}:
                continue
            if relative.casefold() in wanted:
                continue
            safe_path(target_root, relative)
            destination = safe_path(workspace / 'unlisted-files' / folder, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            path.rename(destination)
            leftovers += 1
    print(f'Unlisted files retained in backup: {leftovers}')
    print('Backup and migration evidence: ' + str(workspace), flush=True)


if __name__ == '__main__':
    main()
