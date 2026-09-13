import copy
import hashlib
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from jfcraft_core import Installer, Cancelled, atomic_json, safe_path, validate_manifest
from launcher_service import validate_settings, profile_lock


def file(name, data=b'new', policy='managed'):
    return dict(path=name, size=len(data), sha256=hashlib.sha256(data).hexdigest(), url='https://example.org/mod', policy=policy)


def manifest(*files):
    return dict(schema=1, id='test', name='Test', version='1', minecraft='1.7.10', forge='1.7.10-10.13.4.1614-1.7.10',
                installed_version='1.7.10-Forge10.13.4.1614-1.7.10', java=8, files=list(files))


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.installer = Installer(self.root)

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)

    def download(self, item, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'new')

    def test_bad_paths(self):
        for path in ('../outside', 'mods/../../x', '/tmp/x', 'mods/a:b', 'mods\\x', 'mods/CON.jar', 'mods/a.', 'mods//x'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                safe_path(self.root, path)

    def test_forbid_saves(self):
        with self.assertRaises(ValueError):
            validate_manifest(manifest(file('saves/world.dat')))

    def test_case_collision(self):
        with self.assertRaises(ValueError):
            validate_manifest(manifest(file('mods/A.jar'), file('mods/a.jar')))

    def test_corrupt_same_name_repaired(self):
        self.write('mods/a.jar', b'bad')
        with patch.object(self.installer, 'download', side_effect=self.download) as download:
            self.installer.install(manifest(file('mods/a.jar')))
            download.assert_called_once()
        self.assertEqual((self.root / 'mods/a.jar').read_bytes(), b'new')
        self.assertEqual(next((self.root / '.jfcraft-backups').rglob('a.jar')).read_bytes(), b'bad')

    def test_valid_file_not_downloaded(self):
        self.write('mods/a.jar', b'new')
        with patch.object(self.installer, 'download') as download:
            self.installer.install(manifest(file('mods/a.jar')))
            download.assert_not_called()

    def test_failure_before_commit_preserves_old(self):
        self.write('mods/a.jar', b'old')
        with patch.object(self.installer, 'download', side_effect=OSError('network')), self.assertRaises(OSError):
            self.installer.install(manifest(file('mods/a.jar')))
        self.assertEqual((self.root / 'mods/a.jar').read_bytes(), b'old')
        self.assertFalse((self.root / '.jfcraft-state.json').exists())

    def test_preserve_settings_and_worlds(self):
        self.write('options.txt', b'personal')
        self.write('saves/world/level.dat', b'world')
        self.write('mods/personal.jar', b'mine')
        with patch.object(self.installer, 'download') as download:
            self.installer.install(manifest(file('options.txt', policy='preserve')))
            download.assert_not_called()
        self.assertEqual((self.root / 'options.txt').read_bytes(), b'personal')
        self.assertEqual((self.root / 'saves/world/level.dat').read_bytes(), b'world')
        self.assertTrue((self.root / 'mods/personal.jar').exists())

    def test_remove_only_previously_managed(self):
        self.write('mods/old.jar', b'old')
        self.write('mods/user.jar', b'user')
        atomic_json(self.root / '.jfcraft-state.json', manifest(file('mods/old.jar')))
        self.installer.install(manifest())
        self.assertFalse((self.root / 'mods/old.jar').exists())
        self.assertTrue((self.root / 'mods/user.jar').exists())
        self.assertEqual(next((self.root / '.jfcraft-backups').rglob('old.jar')).read_bytes(), b'old')

    def test_recover_interrupted_update(self):
        self.write('mods/a.jar', b'new')
        self.write('.jfcraft-backups/tx/mods/a.jar', b'old')
        atomic_json(self.root / '.jfcraft-journal.json', dict(backup='.jfcraft-backups/tx', previous={'files': []}, operations=[dict(path='mods/a.jar', existed=True)]))
        self.installer.recover()
        self.assertEqual((self.root / 'mods/a.jar').read_bytes(), b'old')
        self.assertFalse((self.root / '.jfcraft-journal.json').exists())

    def test_cancel_before_writes(self):
        self.installer.cancel.set()
        with self.assertRaises(Cancelled):
            self.installer.install(manifest(file('mods/a.jar')))
        self.assertFalse((self.root / 'mods/a.jar').exists())

    def test_profile_lock(self):
        with profile_lock(self.root):
            with self.assertRaises(ValueError):
                with profile_lock(self.root):
                    pass
        with profile_lock(self.root):
            pass

    def test_settings(self):
        for low, high, name in [('bad', '4096', 'Player'), ('8192', '4096', 'Player'), ('1024', '4096', '../bad')]:
            with self.assertRaises(ValueError):
                validate_settings(dict(min_ram=low, max_ram=high, username=name))


if __name__ == '__main__':
    unittest.main()
