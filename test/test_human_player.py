import unittest
from unittest.mock import patch
from human_player import HumanPlayer

class TestHumanPlayer(unittest.TestCase):

    def setUp(self):
        self.player = HumanPlayer(color='W')

    @patch('builtins.input', side_effect=['0', '1'])  # Szimuláljuk a felhasználói bemenetet
    def test_get_valid_move(self, mock_input):
        valid_moves = [(0, 1), (0, 2), (1, 0)]
        move = self.player.get_valid_move(valid_moves)
        self.assertEqual(move, (0, 1))  # Ellenőrizzük, hogy a várt lépést adja vissza

    @patch('builtins.input', side_effect=['24', '0', '1'])  # Hibás bemenetek szimulálása
    def test_get_valid_move_invalid_first(self, mock_input):
        valid_moves = [(0, 1), (0, 2), (1, 0)]
        move = self.player.get_valid_move(valid_moves)
        self.assertEqual(move, (0, 1))  # A második bemenetnek érvényesnek kell lennie

    @patch('builtins.input', side_effect=['0', '24', '1'])  # Hibás szomszéd szimulálása
    def test_get_valid_move_invalid_neighbor(self, mock_input):
        valid_moves = [(0, 1), (0, 2), (1, 0)]
        move = self.player.get_valid_move(valid_moves)
        self.assertEqual(move, (0, 1))  # A kiválasztott szomszédnak érvényesnek kell lennie

    @patch('builtins.input', side_effect=['0', '1'])  # Érvényes lépés
    def test_make_move(self, mock_input):
        board = ['W'] * 24
        valid_moves = [0, 1, 2, 3]
        move = self.player.make_move(board, valid_moves)
        self.assertIn(move, valid_moves)  # Ellenőrizzük, hogy a visszatérési érték érvényes

    @patch('builtins.input', side_effect=['3', '0'])  # Érvényes darab eltávolítása
    def test_choose_opponent_piece_to_remove(self, mock_input):
        removable_pieces = [0, 1, 2]
        piece = self.player.choose_opponent_piece_to_remove([], removable_pieces)
        self.assertIn(piece, removable_pieces)  # Ellenőrizzük, hogy a választott darab érvényes

if __name__ == '__main__':
    unittest.main()