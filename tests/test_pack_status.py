from pathlib import Path
import tempfile
import unittest
from jfcraft_core import atomic_json
from launcher_service import pack_status
from test_installer import manifest

class PackStatusTests(unittest.TestCase):
    def test_install_update_revision_and_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pack=manifest()
            self.assertEqual(pack_status(pack,root)[0],'missing')
            atomic_json(root/'.jfcraft-state.json',pack)
            self.assertEqual(pack_status(pack,root)[0],'repair')
            version=pack['installed_version']
            atomic_json(root/'versions'/version/(version+'.json'),{})
            self.assertEqual(pack_status(pack,root)[0],'installed')
            self.assertEqual(pack_status(dict(pack,version='new'),root)[0],'update')
            self.assertEqual(pack_status(dict(pack,manifest_revision=1),root)[0],'update')
            self.assertEqual(pack_status(dict(pack,description='new description'),root)[0],'installed')
            atomic_json(root/'.jfcraft-journal.json',{})
            self.assertEqual(pack_status(pack,root)[0],'repair')
