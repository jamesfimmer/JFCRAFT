import json
from pathlib import Path
import tempfile
import unittest

from tools.build_pack import build


class BuildPackTests(unittest.TestCase):
    def build(self, source, output):
        return build(source, output, 'test', 'Test', '1.0', '1.20.1',
                     '1.20.1-47.3.0', '1.20.1-forge-47.3.0', 17,
                     'jamesfimmer/JFCRAFT', 'Test Pack')

    def test_writes_json_and_keeps_zip_as_direct_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            (source / 'shaderpacks').mkdir(parents=True)
            (source / 'shaderpacks/A pack.zip').write_bytes(b'pack')
            (source / 'saves').mkdir()
            (source / 'saves/level.dat').write_bytes(b'world')
            output = root / 'packs/test.json'
            pack = self.build(source, output)
            self.assertTrue(output.is_file())
            self.assertEqual(json.loads(output.read_text()), pack)
            self.assertEqual(len(pack['files']), 1)
            self.assertNotIn('archive', pack['files'][0])
            self.assertIn('/main/download-files/Test%20Pack/shaderpacks/A%20pack.zip', pack['files'][0]['url'])

    def test_outer_archive_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'source'
            source.mkdir()
            (source / 'shaderpacks.rar').write_bytes(b'container')
            with self.assertRaises(ValueError):
                self.build(source, root / 'pack.json')
            self.assertFalse((root / 'pack.json').exists())
