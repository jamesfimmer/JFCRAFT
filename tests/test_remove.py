import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from launcher_service import remove_pack, profile_lock


class RemoveTests(unittest.TestCase):
    def test_removal_preserves_world_and_mod_bytes_in_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            root = home / 'instances' / 'test'
            for name in ['saves/My World/level.dat', 'mods/mod.jar', '.jfcraft-state.json']:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'original bytes')
            with patch('launcher_service.data_dir', return_value=home):
                backup = remove_pack('test')
            self.assertEqual((backup / 'saves/My World/level.dat').read_bytes(), b'original bytes')
            self.assertEqual((backup / 'mods/mod.jar').read_bytes(), b'original bytes')
            self.assertFalse((root / '.jfcraft-state.json').exists())

    def test_running_profile_cannot_be_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with patch('launcher_service.data_dir', return_value=home), profile_lock(home / 'instances/test'):
                with self.assertRaises(ValueError):
                    remove_pack('test')
