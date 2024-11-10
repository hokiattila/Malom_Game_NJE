import unittest
from random_player import RandomPlayer

class TestRandomPlayer(unittest.TestCase):

    def setUp(self):
        self.player = RandomPlayer("W")  # Létrehozunk egy RandomPlayer példányt

    def test_make_move_with_valid_moves(self):
        board = ["W", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]  # Példa tábla
        valid_moves = [0, 1, 2]  # Érvényes lépések
        move = self.player.make_move(board, valid_moves)
        self.assertIn(move, valid_moves)  # Ellenőrizzük, hogy a kiválasztott lépés az érvényes lépések között van

    def test_make_move_with_no_valid_moves(self):
        board = ["W", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
        valid_moves = []  # Nincsenek érvényes lépések
        move = self.player.make_move(board, valid_moves)
        self.assertIsNone(move)  # Ellenőrizzük, hogy None-t ad vissza

    def test_choose_opponent_piece_to_remove(self):
        board = ["W", "B", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] 
        removable_pieces = [1, 2]  # Eltávolítható korongok
        piece_to_remove = self.player.choose_opponent_piece_to_remove(board, removable_pieces)
        self.assertIn(piece_to_remove, removable_pieces)  # Ellenőrizzük, hogy a kiválasztott korong az eltávolítható korongok között van

if __name__ == "__main__":
    unittest.main()