import os
import subprocess
import sys
import time
import unittest
from game_process import WindowsGame
from launcher_service import GameProcess

@unittest.skipUnless(os.name == 'nt', 'Windows jobs')
class WindowsGameTests(unittest.TestCase):
    def test_child_survives_parent_and_owned_tree_can_be_stopped(self):
        outsider = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])
        game = None
        try:
            child_code = 'import time; time.sleep(30)'
            parent_code = 'import subprocess,sys; subprocess.Popen([sys.executable,"-c",' + repr(child_code) + '])'
            game = WindowsGame([sys.executable, '-c', parent_code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            game.process.wait(timeout=10)
            self.assertIsNone(game.poll(), 'Child must keep game session alive after parent exits')
            owner = GameProcess()
            owner.attach(game)
            self.assertTrue(owner.running())
            self.assertTrue(owner.stop())
            deadline = time.monotonic() + 10
            while game.poll() is None and time.monotonic() < deadline:
                time.sleep(.05)
            self.assertIsNotNone(game.poll())
            self.assertIsNone(outsider.poll(), 'Unrelated process must survive')
            owner.detach()
        finally:
            if game is not None:
                game.terminate_tree()
                game.close()
            outsider.kill()
            outsider.wait()

    def test_normal_exit(self):
        game = WindowsGame([sys.executable, '-c', 'pass'])
        try:
            self.assertEqual(game.wait(), 0)
        finally:
            game.close()
