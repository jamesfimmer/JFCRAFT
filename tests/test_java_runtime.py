import hashlib
import io
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, Mock, patch
import zipfile
from jfcraft_core import Cancelled
from java_runtime import find_java, install_java
from launcher_service import resolve_java

class JavaRuntimeTests(unittest.TestCase):
    def test_local_java_without_network(self):
        with patch('java_runtime.candidates', return_value=['wrong', 'cached']), patch('requests.get', side_effect=AssertionError('network')):
            verify=Mock(side_effect=[ValueError(), 'cached'])
            self.assertEqual(find_java(21, Path('.'), '', verify, threading.Event()), 'cached')

    def install(self, home, filename='jre/bin/java.exe', bad_hash=False):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as z:
            z.writestr(filename, b'java')
        content=stream.getvalue()
        metadata=MagicMock()
        metadata.__enter__.return_value=metadata
        metadata.json.return_value=[{'binary':{'package':{'link':'https://example.com/java.zip','size':len(content),'checksum':'0'*64 if bad_hash else hashlib.sha256(content).hexdigest()}}}]
        response=MagicMock()
        response.__enter__.return_value=response
        response.url='https://example.com/java.zip'
        response.iter_content.side_effect=lambda *a: iter([content])
        with patch('requests.get',side_effect=[metadata,response,response,response]):
            return install_java(21,home,lambda p,v:p,Mock(),Mock(),threading.Event())

    def test_install_then_discover_cached_runtime(self):
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            java=self.install(home/'java-21')
            self.assertEqual(Path(java).read_bytes(),b'java')
            with patch('requests.get',side_effect=AssertionError('network')):
                self.assertEqual(find_java(21,home,'',lambda p,v:p,threading.Event()),java)

    def test_corrupt_download_and_traversal_do_not_publish(self):
        for filename,bad in [('jre/bin/java.exe',True),('../escape.exe',False)]:
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as tmp:
                home=Path(tmp)
                with self.assertRaises(ValueError):
                    self.install(home,filename,bad)
                self.assertEqual(list(home.iterdir()),[])

    def test_cancel_and_offline_missing_runtime_do_not_download(self):
        event=threading.Event(); event.set()
        with patch('requests.get',side_effect=AssertionError('network')):
            with self.assertRaises(Cancelled):
                install_java(21,Path('.'),Mock(),Mock(),Mock(),event)
        with patch('launcher_service.find_java',return_value=None),patch('launcher_service.install_java') as install:
            with self.assertRaises(ValueError):
                resolve_java(21,'',Mock(),Mock(),threading.Event(),False)
            install.assert_not_called()
