import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from jfcraft_core import Installer
from test_installer import file, manifest


class ArchiveTests(unittest.TestCase):
    def test_only_manifest_member_extracted_and_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'instance'
            archive = Path(temp) / 'pack.zip'
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('a.cfg', b'new')
                bundle.writestr('../escaped.txt', b'bad')
            content = archive.read_bytes()
            item = file('config/a.cfg')
            item['archive'] = dict(member='a.cfg', url=item['url'], size=len(content), sha256=hashlib.sha256(content).hexdigest())
            installer = Installer(root)
            def download(item, target):
                target.parent.mkdir(parents=True)
                target.write_bytes(content)
            with patch.object(installer, 'download', side_effect=download):
                installer.install(manifest(item))
            self.assertEqual((root / 'config/a.cfg').read_bytes(), b'new')
            self.assertFalse((Path(temp) / 'escaped.txt').exists())

    def test_archive_wrong_content_prevents_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'instance'
            archive = Path(temp) / 'pack.zip'
            with zipfile.ZipFile(archive, 'w') as bundle:
                bundle.writestr('a.cfg', b'bad')
            content = archive.read_bytes()
            item = file('config/a.cfg')
            item['archive'] = dict(member='a.cfg', url=item['url'], size=len(content), sha256=hashlib.sha256(content).hexdigest())
            installer = Installer(root)
            def download(item, target):
                target.parent.mkdir(parents=True)
                target.write_bytes(content)
            with patch.object(installer, 'download', side_effect=download), self.assertRaises(ValueError):
                installer.install(manifest(item))
            self.assertFalse((root / 'config/a.cfg').exists())
