import unittest
from unittest.mock import Mock, patch
from launcher_service import GameProcess

class GameProcessTests(unittest.TestCase):
    def test_stops_only_owned_process_tree(self):
        game = GameProcess()
        process = Mock(pid=12345)
        process.poll.return_value = None
        game.attach(process)
        with patch('launcher_service.subprocess.run', return_value=Mock(returncode=0)) as run:
            self.assertTrue(game.stop())
        self.assertEqual(run.call_args.args[0], ['taskkill', '/PID', '12345', '/T', '/F'])
        self.assertTrue(game.stopped)
        game.detach()
        self.assertFalse(game.running())

    def test_exited_or_missing_process_is_not_killed(self):
        game = GameProcess()
        with patch('launcher_service.subprocess.run') as run:
            self.assertFalse(game.stop())
            process = Mock()
            process.poll.return_value = 0
            game.attach(process)
            self.assertFalse(game.stop())
            run.assert_not_called()

    def test_failure_is_not_reported_as_user_stop(self):
        game = GameProcess()
        process = Mock(pid=12345)
        process.poll.return_value = None
        game.attach(process)
        with patch('launcher_service.subprocess.run', return_value=Mock(returncode=1)):
            with self.assertRaises(RuntimeError):
                game.stop()
        self.assertFalse(game.stopped)
