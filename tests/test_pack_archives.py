"""Regression coverage for real RAR containers holding ZIP packs."""
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import zipfile
import subprocess

from jfcraft_archives import archive_member, rar_members
from jfcraft_core import Installer

ROOT = Path(__file__).resolve().parents[1]


class PackArchiveTests(unittest.TestCase):
    def test_outer_rar_returns_shader_zip_not_shader_sources(self):
        source = ROOT / 'download-files/Middle-Earth-Chronicles-1.7.10/shaderpacks.rar'
        member = 'shaderpacks/SEUS-Renewed-v1.0.1.zip'
        self.assertIn(member, rar_members(source))
        with archive_member(source, member, 'rar') as stream:
            content = stream.read()
        with zipfile.ZipFile(io.BytesIO(content)) as shader:
            self.assertTrue(any(name.startswith('shaders/') for name in shader.namelist()))

    def test_all_pack_assets_install_as_intact_zip_files(self):
        for path in sorted((ROOT / 'packs').glob('*.json')):
            pack = json.loads(path.read_text(encoding='utf-8'))
            pack['files'] = [f for f in pack['files'] if f['path'].startswith(('shaderpacks/', 'resourcepacks/'))]
            with self.subTest(pack=pack['id']), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                installer = Installer(root)
                def local_download(item, target):
                    # Reproduce the bytes at the URL, not a potentially different
                    # working-tree copy. Installer itself extracts archive members.
                    parts = unquote(urlsplit(item['url']).path).split('/')
                    commit, relative = parts[3], '/'.join(parts[4:])
                    content = subprocess.check_output(
                        ['git', 'show', f'{commit}:{relative}'], cwd=ROOT)
                    self.assertEqual(len(content), item['size'])
                    self.assertEqual(hashlib.sha256(content).hexdigest(), item['sha256'])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
                with patch.object(installer, 'download', side_effect=local_download):
                    installer.install(pack)
                for item in pack['files']:
                    installed = root / item['path']
                    self.assertEqual(hashlib.sha256(installed.read_bytes()).hexdigest(), item['sha256'])
                    if installed.suffix == '.zip':
                        self.assertTrue(zipfile.is_zipfile(installed))
                self.assertFalse((root / 'shaderpacks/shaders').exists())
                self.assertFalse((root / 'resourcepacks/assets').exists())
