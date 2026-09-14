import tempfile
import threading
import unittest
import requests
from pathlib import Path
from unittest.mock import patch, Mock

from jfcraft_core import atomic_json
from launcher_service import run_pack
from test_installer import manifest


class OfflineTests(unittest.TestCase):
    def test_unreachable_updates_use_installed_version_without_installer(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            pack = manifest()
            root = home / 'instances' / pack['id']
            atomic_json(root / '.jfcraft-state.json', pack)
            atomic_json(root / 'versions' / pack['installed_version'] / (pack['installed_version'] + '.json'), {})
            (root / 'mods').mkdir()
            (root / 'mods/extra.jar').write_bytes(b'extra')
            advertised = dict(pack, installed_version='not-installed', version='future')
            process = Mock()
            process.wait.return_value = 0
            with patch('launcher_service.data_dir', return_value=home), \
                 patch('launcher_service.check_java', return_value='java'), \
                 patch('launcher_service.refresh_pack', side_effect=requests.ConnectionError('offline')), \
                 patch('launcher_service.ensure_forge', side_effect=AssertionError('runtime install')), \
                 patch('launcher_service.Installer.install', side_effect=AssertionError('pack install')), \
                 patch('requests.sessions.Session.request', side_effect=AssertionError('network')), \
                 patch('minecraft_launcher_lib.command.get_minecraft_command', return_value=['java']) as command, \
                 patch('launcher_service.subprocess.Popen', return_value=process):
                run_pack(advertised, {'username': 'Player', 'min_ram': 1024, 'max_ram': 2048},
                         True, lambda m: None, lambda v, t: None, threading.Event())
                self.assertEqual(command.call_args.args[0], pack['installed_version'])
                self.assertFalse((root / 'mods/extra.jar').exists())
