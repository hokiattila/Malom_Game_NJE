import unittest
from greedy_player import GreedyPlayer

class TestGreedyPlayer(unittest.TestCase):

    def setUp(self):
        self.player = GreedyPlayer(color='W')

    def test_choose_best_placement_completes_mill(self):
        board = ['W', 'W', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        valid_moves = [2, 3]
        move = self.player.make_move(board, valid_moves)
        self.assertEqual(move, 2, "Should complete a mill by placing at position 2")

    def test_choose_best_placement_blocks_opponent_mill(self):
        board = [' ', ' ', 'B', 'B', ' ', ' ', ' ', ' ', ' ']
        valid_moves = [0, 1, 4]
        move = self.player.make_move(board, valid_moves)
        self.assertIn(move, [0, 1], "Should block opponent's mill")

    def test_choose_best_move_completes_mill(self):
        board = [' ', ' ', ' ', 'W', ' ', ' ', ' ', ' ', ' ']
        valid_moves = [(3, 0), (3, 1)]
        move = self.player.make_move(board, valid_moves)
        self.assertEqual(move, (3, 0), "Should complete a mill with the move")

    def test_choose_opponent_piece_to_remove(self):
        board = ['W', 'W', ' ', 'B', 'B', ' ']
        removable_pieces = [3, 4]
        move = self.player.choose_opponent_piece_to_remove(board, removable_pieces)
        self.assertIn(move, [3, 4], "Should remove one of the removable opponent pieces")

    def test_choose_opponent_piece_to_remove_non_mill(self):
        board = ['W', 'W', ' ', 'B', 'B', 'B']
        removable_pieces = [3, 4]
        move = self.player.choose_opponent_piece_to_remove(board, removable_pieces)
        self.assertEqual(move, 3, "Should remove the first opponent piece not in a mill")

if __name__ == "__main__":
    unittest.main()