import unittest
from unittest.mock import patch, MagicMock
import sys
from main import Game

class TestMain(unittest.TestCase):

    @patch('engine.game.Game')
    @patch('sys.exit')
    def test_main_debug_mode_enabled(self, mock_exit, mock_game):
        # Mock arguments
        test_args = [
            'main.py',
            '--debug',
            '--log',
            '--mode', 'pvc',
            '--diff', 'easy'
        ]
        with patch.object(sys, 'argv', test_args):
            import main  # Import after patching

        # Assert that Game was called with correct parameters
        mock_game.assert_called_once_with(mode='pvc', debug=True, log=True, difficulty='easy', p1_flag=None, p2_flag=None)
        
    @patch('engine.game.Game')
    @patch('sys.exit')
    def test_main_debug_mode_disabled(self, mock_exit, mock_game):
        # Mock arguments
        test_args = [
            'main.py',
            '--mode', 'pvp'
        ]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):  # Expecting the program to exit
                import main  # Import after patching

        mock_exit.assert_called_once_with('At the moment only debug mode is supported')

    @patch('engine.game.Game')
    def test_game_initialization_with_cvc_mode(self, mock_game):
        # Mock arguments
        test_args = [
            'main.py',
            '--debug',
            '--mode', 'cvc',
            '--p1', 'greedy',
            '--p2', 'astar'
        ]
        with patch.object(sys, 'argv', test_args):
            import main  # Import after patching

        # Assert that Game was called with the correct parameters
        mock_game.assert_called_once_with(mode='cvc', debug=True, log=False, difficulty=None, p1_flag='greedy', p2_flag='astar')

if __name__ == '__main__':
    unittest.main()