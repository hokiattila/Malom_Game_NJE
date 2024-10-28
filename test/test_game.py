import unittest
from game import Game
from engine.player.human_player import HumanPlayer
from engine.player.greedy_player import GreedyPlayer

class TestGame(unittest.TestCase):

    def setUp(self):
        # Játék beállítása minden teszt előtt
        self.game = Game(mode="pvp", debug=True)

    def test_initial_conditions(self):
        self.assertEqual(self.game.turn_player1, True)
        self.assertEqual(self.game.pieces_placed_player1, 0)
        self.assertEqual(self.game.pieces_placed_player2, 0)
        self.assertEqual(len(self.game.board), 24)

    def test_switch_turns(self):
        initial_turn = self.game.turn_player1
        self.game.switch_turns()
        self.assertNotEqual(initial_turn, self.game.turn_player1)

    def test_register_move_placing(self):
        self.game.register_move(0)  # 1. játékos egy bábut helyez el a 0. pozícióra
        self.assertEqual(self.game.board[0], 'W')  # 1. játékos bábujának a 0. pozícióban kell lennie
        self.assertEqual(self.game.pieces_placed_player1, 1)

    def test_register_move_moving(self):
        # Először helyezzen el egy bábut
        self.game.register_move(0)  # 1. játékos bábut helyez el a 0. pozícióra
        self.game.switch_turns()
        self.game.register_move(1)  # 2. játékos bábut helyez el az 1. pozícióra
        self.game.switch_turns()

        self.game.register_move(0, 1)  # Mozdítsa a 0. pozícióból az 1. pozícióba
        self.assertEqual(self.game.board[1], 'W')  # 1. játékos bábujának most az 1. pozícióban kell lennie
        self.assertEqual(self.game.board[0], '0')  # A 0. pozíciónak üresnek kell lennie

    def test_remove_opponent_piece(self):
        self.game.register_move(0)  # 1. játékos bábut helyez el a 0. pozícióra
        self.game.switch_turns()
        self.game.register_move(1)  # 2. játékos bábut helyez el az 1. pozícióra
        self.game.switch_turns()

        self.game.register_move(0, 1)  # 1. játékos bábut mozgat a 0. pozícióból az 1. pozícióba
        self.game.remove_opponent_piece()  # 1. játékos eltávolítja a 2. játékos bábuját

        self.assertEqual(self.game.board[1], '0')  # A 2. játékos bábujának el kell tűnnie
        self.assertEqual(self.game.board[0], 'W')  # 1. játékos bábujának a 0. pozícióban kell maradnia

    def test_game_over_conditions(self):
        # Játékvégi feltételek tesztelése, amikor a játékosnak kevesebb mint 3 bábuja van
        for i in range(9):  # 1. játékos 9 bábut helyez el
            self.game.register_move(i)
        self.game.switch_turns()
        for i in range(1, 10):  # 2. játékos 9 bábut helyez el
            self.game.register_move(i)

        # Eltávolítunk néhány bábút a 2. játékostól, hogy szimuláljuk a játék végét
        self.game.register_move(1, 0)  # Mozgassuk a 2. játékos bábuját
        self.game.remove_opponent_piece()  # 1. játékos eltávolítja a 2. játékos bábuját
        self.game.remove_opponent_piece()  # Eltávolítunk még egy bábút

        # Ellenőrizzük, hogy a játék vége van-e, mivel a 2. játékosnak kevesebb mint 3 bábúja van
        self.assertTrue(self.game.game_over())

    def test_generate_valid_moves(self):
        self.game.register_move(0)  # 1. játékos bábut helyez el a 0. pozícióra
        self.game.switch_turns()
        self.game.register_move(1)  # 2. játékos bábut helyez el az 1. pozícióra
        self.game.switch_turns()

        valid_moves = self.game.generate_valid_moves()
        self.assertIn((0, 1), valid_moves)  # Lehetővé kell tenni a 0-ból 1-be való mozgást
        self.assertIn((1, 2), valid_moves)  # Lehetővé kell tenni az 1-ből 2-be való mozgást, ha az üres

if __name__ == '__main__':
    unittest.main()
