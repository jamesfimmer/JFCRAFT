import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from launcher_service import sync_catalog
from test_installer import manifest
from jfcraft_core import atomic_json

class CatalogTests(unittest.TestCase):
    def test_background_fetch_does_not_write_and_keeps_newer_cached_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            pack=manifest(); pack['manifest_revision']=2
            path=root/'manifests'/ (pack['id']+'.json')
            atomic_json(path,pack)
            response=Mock(); response.json.return_value={'schema':1,'packs':[pack['id']]}
            remote=dict(pack,manifest_revision=1)
            with patch('launcher_service.data_dir',return_value=root),patch('launcher_service.resource_dir',return_value=root/'bundled'),patch('launcher_service.requests.get',return_value=response),patch('launcher_service.load_manifest',side_effect=[remote,pack]),patch('launcher_service.atomic_json') as write:
                result=sync_catalog(Mock(),persist=False)
                write.assert_not_called()
                self.assertEqual(result[0]['manifest_revision'],2)
