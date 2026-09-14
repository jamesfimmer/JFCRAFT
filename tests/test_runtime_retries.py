import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
import requests
from urllib3.exceptions import ProtocolError

from jfcraft_core import Cancelled, atomic_json
from launcher_service import ensure_forge
from test_installer import manifest


class RuntimeRetryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.pack = manifest()
        self.cancel = Mock(is_set=Mock(return_value=False), wait=Mock(return_value=False))
        self.messages = []

    def install(self):
        ensure_forge(self.pack, self.root, 'java', self.messages.append, self.cancel)

    def test_raw_stream_disconnect_is_retried_before_marking_success(self):
        calls = []
        def attempt(*args, **kwargs):
            calls.append(1)
            self.assertFalse((self.root / '.jfcraft-runtime.json').exists())
            if len(calls) == 1:
                raise ProtocolError('Connection broken: IncompleteRead')
            version = self.pack['installed_version']
            atomic_json(self.root / 'versions' / version / (version + '.json'), {'id': version})
        with patch('minecraft_launcher_lib.forge.install_forge_version', side_effect=attempt), patch('launcher_service.logging.warning'):
            self.install()
        self.assertEqual(len(calls), 2)
        self.assertTrue((self.root / '.jfcraft-runtime.json').exists())
        self.assertTrue(any('2/3' in m for m in self.messages))

    def test_three_failures_stop_without_success_marker(self):
        with patch('minecraft_launcher_lib.forge.install_forge_version', side_effect=ProtocolError('broken')) as install, patch('launcher_service.logging.warning'):
            with self.assertRaises(requests.ConnectionError):
                self.install()
        self.assertEqual(install.call_count, 3)
        self.assertFalse((self.root / '.jfcraft-runtime.json').exists())

    def test_cancel_during_retry_does_not_start_another_attempt(self):
        def wait(seconds):
            self.cancel.is_set.return_value = True
            return True
        self.cancel.wait.side_effect = wait
        with patch('minecraft_launcher_lib.forge.install_forge_version', side_effect=ProtocolError('broken')) as install, patch('launcher_service.logging.warning'):
            with self.assertRaises(Cancelled):
                self.install()
        self.assertEqual(install.call_count, 1)

    def test_non_network_error_is_not_retried(self):
        with patch('minecraft_launcher_lib.forge.install_forge_version', side_effect=ValueError('invalid profile')) as install:
            with self.assertRaises(ValueError):
                self.install()
        self.assertEqual(install.call_count, 1)
