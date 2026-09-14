from contextlib import ExitStack
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch
import requests

from jfcraft_core import Installer, Cancelled, atomic_json, load_manifest
from launcher_service import run_pack
from test_installer import file, manifest


class PlayUpdateTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.home = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.old = manifest(file('mods/old.jar', b'old'))
        self.latest = dict(manifest(file('mods/new.jar', b'new')), version='2')
        self.root = self.home / 'instances/test'
        self.cancel = threading.Event()
        self.stack.enter_context(patch('launcher_service.data_dir', return_value=self.home))
        self.stack.enter_context(patch('launcher_service.check_java', return_value='java'))
        self.refresh = self.stack.enter_context(patch('launcher_service.refresh_pack', return_value=self.latest))
        self.forge = self.stack.enter_context(patch('launcher_service.ensure_forge'))
        self.command = self.stack.enter_context(patch('minecraft_launcher_lib.command.get_minecraft_command', return_value=['java']))
        self.process = self.stack.enter_context(patch('launcher_service.subprocess.Popen', return_value=Mock(wait=Mock(return_value=0))))

    def installed(self):
        atomic_json(self.root / '.jfcraft-state.json', self.old)
        version = self.old['installed_version']
        atomic_json(self.root / 'versions' / version / (version + '.json'), {})
        (self.root / 'mods').mkdir()
        (self.root / 'mods/old.jar').write_bytes(b'old')

    def play(self):
        run_pack(self.old, dict(username='Player', min_ram=1024, max_ram=2048),
                 True, lambda m: None, lambda v, t: None, self.cancel)

    def download(self, item, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'new')

    def test_play_updates_files_before_launch(self):
        self.installed()
        with patch.object(Installer, 'download', side_effect=self.download):
            self.play()
        self.assertEqual(load_manifest(self.root / '.jfcraft-state.json')['version'], '2')
        self.assertFalse((self.root / 'mods/old.jar').exists())
        self.assertEqual((self.root / 'mods/new.jar').read_bytes(), b'new')
        self.process.assert_called_once()
        self.forge.assert_not_called()

    def test_download_disconnect_launches_previous_intact_pack(self):
        self.installed()
        with patch.object(Installer, 'download', side_effect=requests.Timeout):
            self.play()
        self.assertEqual(load_manifest(self.root / '.jfcraft-state.json')['version'], '1')
        self.assertEqual((self.root / 'mods/old.jar').read_bytes(), b'old')
        self.process.assert_called_once()

    def test_first_play_installs_then_launches(self):
        with patch.object(Installer, 'download', side_effect=self.download):
            self.play()
        self.forge.assert_called_once()
        self.process.assert_called_once()

    def test_first_play_without_network_does_not_launch(self):
        self.refresh.side_effect = requests.ConnectionError
        with self.assertRaises(ValueError):
            self.play()
        self.process.assert_not_called()

    def test_bad_checksum_does_not_silently_launch(self):
        self.installed()
        with patch.object(Installer, 'download', side_effect=ValueError('checksum')), self.assertRaises(ValueError):
            self.play()
        self.process.assert_not_called()

    def test_cancel_does_not_trigger_fallback(self):
        self.installed()
        self.cancel.set()
        with self.assertRaises(Cancelled):
            self.play()
        self.refresh.assert_not_called()
        self.process.assert_not_called()
