"""Exercise direct pack downloads against every checked-in manifest."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit
import zipfile

from jfcraft_core import Installer

ROOT = Path(__file__).resolve().parents[1]


class PackArchiveTests(unittest.TestCase):
    def test_shader_zip_remains_a_complete_pack(self):
        source = ROOT / 'download-files/Middle-Earth-Chronicles-1.7.10/shaderpacks/SEUS-Renewed-v1.0.1.zip'
        with zipfile.ZipFile(source) as shader:
            self.assertTrue(any(name.startswith('shaders/') for name in shader.namelist()))

    def test_all_pack_assets_install_as_intact_zip_files(self):
        for path in sorted((ROOT / 'packs').glob('*.json')):
            pack = json.loads(path.read_text(encoding='utf-8'))
            with self.subTest(pack=pack['id']), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                installer = Installer(root)
                def local_download(item, target):
                    self.assertNotIn('archive', item)
                    parts = unquote(urlsplit(item['url']).path).split('/')
                    relative = '/'.join(parts[4:])
                    content = (ROOT / relative).read_bytes()
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
