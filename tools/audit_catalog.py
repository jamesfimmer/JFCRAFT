"""Check every downloadable asset against exact Git blobs (no text conversion)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from jfcraft_core import validate_manifest


def main():
    assets = {}
    entries = 0
    for path in sorted((ROOT / 'packs').glob('*.json')):
        pack = json.loads(path.read_text(encoding='utf-8'))
        validate_manifest(pack)
        entries += len(pack['files'])
        for item in pack['files']:
            asset = item.get('archive', item)
            expected = (asset['size'], asset['sha256'])
            if asset['url'] in assets and assets[asset['url']] != expected:
                raise ValueError('Conflicting checksums for ' + asset['url'])
            assets[asset['url']] = expected
    process = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for url, expected in assets.items():
            parts = unquote(urlsplit(url).path).split('/')
            commit, path = parts[3], '/'.join(parts[4:])
            process.stdin.write(f'{commit}:{path}\n'.encode('utf-8'))
            process.stdin.flush()
            header = process.stdout.readline().split()
            if len(header) != 3 or header[1] != b'blob':
                raise ValueError('Missing Git asset: ' + url)
            size = remaining = int(header[2])
            digest = hashlib.sha256()
            while remaining:
                block = process.stdout.read(min(1024 * 1024, remaining))
                if not block:
                    raise EOFError(url)
                digest.update(block)
                remaining -= len(block)
            assert process.stdout.read(1) == b'\n'
            if (size, digest.hexdigest()) != expected:
                raise ValueError('Asset mismatch: ' + url)
    finally:
        process.stdin.close()
        process.stdout.close()
        process.wait(timeout=10)
    print(f'AUDIT_OK: {entries} entries, {len(assets)} unique assets match exact Git blobs')


if __name__ == '__main__':
    main()
