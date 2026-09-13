import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import requests

from jfcraft_core import Installer, atomic_json
from launcher_service import refresh_pack
from test_installer import file, manifest


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = manifest(file('mods/a.jar'))
        self.pack['update_url'] = 'https://example.org/latest.json'

    def test_updates_manifest_and_remembers_channel(self):
        latest = manifest(file('mods/b.jar'))
        latest['version'] = '2'
        with patch('launcher_service.data_dir', return_value=self.root), patch('launcher_service.load_manifest', return_value=latest):
            actual = refresh_pack(self.pack, lambda m: None)
        self.assertEqual(actual['version'], '2')
        self.assertEqual(actual['update_url'], self.pack['update_url'])
        self.assertTrue((self.root / 'manifests/test.json').exists())

    def test_network_failure_uses_saved_manifest(self):
        with patch('launcher_service.data_dir', return_value=self.root), patch('launcher_service.load_manifest', side_effect=requests.Timeout):
            self.assertEqual(refresh_pack(self.pack, lambda m: None), self.pack)

    def test_wrong_pack_rejected(self):
        latest = manifest()
        latest['id'] = 'another'
        with patch('launcher_service.data_dir', return_value=self.root), patch('launcher_service.load_manifest', return_value=latest), self.assertRaises(ValueError):
            refresh_pack(self.pack, lambda m: None)

    def test_merge_updates_untouched_config(self):
        path = self.root / 'config/a.cfg'
        path.parent.mkdir()
        path.write_bytes(b'old')
        atomic_json(self.root / '.jfcraft-state.json', manifest(file('config/a.cfg', b'old', 'merge')))
        installer = Installer(self.root)
        def download(item, target):
            target.parent.mkdir(parents=True)
            target.write_bytes(b'new')
        with patch.object(installer, 'download', side_effect=download):
            installer.install(manifest(file('config/a.cfg', b'new', 'merge')))
        self.assertEqual(path.read_bytes(), b'new')

    def test_merge_preserves_edited_config(self):
        path = self.root / 'config/a.cfg'
        path.parent.mkdir()
        path.write_bytes(b'my settings')
        atomic_json(self.root / '.jfcraft-state.json', manifest(file('config/a.cfg', b'old', 'merge')))
        installer = Installer(self.root)
        with patch.object(installer, 'download') as download:
            installer.install(manifest(file('config/a.cfg', b'new', 'merge')))
            download.assert_not_called()
        self.assertEqual(path.read_bytes(), b'my settings')

    def test_checksum_failure_never_commits(self):
        class Response:
            url = 'https://example.org/mod'
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def raise_for_status(self): pass
            def iter_content(self, size): yield b'bad'
        installer = Installer(self.root)
        with patch('jfcraft_core.requests.get', return_value=Response()), patch.object(installer.cancel, 'wait', return_value=False), self.assertRaises(ValueError):
            installer.install(manifest(file('mods/a.jar')))
        self.assertFalse((self.root / 'mods/a.jar').exists())


if __name__ == '__main__':
    unittest.main()
