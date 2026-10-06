import json
from pathlib import Path
import tempfile
import unittest
from build_pack_ui import create_pack

class BuilderTests(unittest.TestCase):
    def test_generation_registration_and_invalid_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'download-files/My Pack'
            source.mkdir(parents=True)
            (source / 'options.txt').write_bytes(b'music:0')
            catalog = root / 'packs/catalog/index.json'
            catalog.parent.mkdir(parents=True)
            catalog.write_text('{"schema":1,"packs":["old"]}')
            fields = dict(id='new', name='New', version='1', minecraft='1.7.10', forge='1.7.10-test', installed_version='forge-test', java='8', repository='jamesfimmer/JFCRAFT')
            output, data = create_pack(root, source, fields)
            self.assertEqual(data['files'][0]['policy'], 'preserve')
            self.assertIn('My%20Pack/options.txt', data['files'][0]['url'])
            create_pack(root, source, fields)
            self.assertEqual(json.loads(catalog.read_text())['packs'], ['old', 'new'])
            original = output.read_bytes()
            catalog.write_text('{}')
            with self.assertRaises(ValueError):
                create_pack(root, source, fields)
            self.assertEqual(output.read_bytes(), original)
            with self.assertRaises(ValueError):
                create_pack(root, root, fields, False)
            fields['id'] = '../escape'
            with self.assertRaises(ValueError):
                create_pack(root, source, fields, False)
