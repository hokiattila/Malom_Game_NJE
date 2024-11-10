import unittest
from ml_player import MLPlayer

class TestMLPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = MLPlayer("W")  # Példa: "W" színű játékos létrehozása
    
    def test_initialization(self):
        self.assertEqual(self.player.color, "W")
        self.assertEqual(self.player.name, "MLPlayer")

    def test_make_move_empty(self):
        # Ellenőrizzük, hogy a make_move metódus None-t ad vissza, ha üres a valid_moves
        result = self.player.make_move([], [])
        self.assertIsNone(result)

    def test_choose_opponent_piece_to_remove_empty(self):
        # Ellenőrizzük, hogy a choose_opponent_piece_to_remove metódus None-t ad vissza, ha üres a removable_pieces
        result = self.player.choose_opponent_piece_to_remove([], [])
        self.assertIsNone(result)

    # Ide jöhetnek további tesztek, ha az implementációk készen állnak

if __name__ == "__main__":
    unittest.main()