import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from launcher_service import prepare_lwjgl_relauncher

class RelauncherTests(unittest.TestCase):
    def test_relocates_java_and_preserves_settings_and_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            config=root/'config/lwjgl3ify-relauncher.json'
            java=root/'config/lotr/runtime/jdk-21/bin/java.exe'
            java.parent.mkdir(parents=True)
            java.write_bytes(b'fake')
            original=dict(javaInstallationsCache=['C:/missing/java.exe'], javaInstallation=0, maxMemoryMB=4096)
            config.write_text(json.dumps(original))
            pack={'files':[{'path':'mods/lwjgl3ify-3.jar'}, {'path':java.relative_to(root).as_posix()}]}
            with patch('launcher_service.check_java', return_value=str(java.resolve())) as check:
                prepare_lwjgl_relauncher(pack,root,lambda m:None)
                prepare_lwjgl_relauncher(pack,root,lambda m:None)
            check.assert_called_once()
            result=json.loads(config.read_text())
            self.assertEqual(result['javaInstallationsCache'],[str(java.resolve())])
            self.assertEqual(result['maxMemoryMB'],4096)
            self.assertTrue(result['forwardLogs'])
            self.assertEqual(json.loads(config.with_suffix('.json.before-java-path-fix').read_text()),original)

    def test_ordinary_pack_is_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            prepare_lwjgl_relauncher({'files':[]},Path(tmp),lambda m:None)
