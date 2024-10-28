import unittest
from a_star_player import AStarPlayer

class TestAStarPlayer(unittest.TestCase):
    
    def setUp(self):
        # Példányosítunk egy AStarPlayer objektumot a tesztek előtt
        self.player = AStarPlayer("red")

    def test_initialization(self):
        # Ellenőrizzük, hogy a szín és a név megfelelően lett beállítva
        self.assertEqual(self.player.color, "red")
        self.assertEqual(self.player.name, "AStarPlayer")

    def test_choose_opponent_piece_to_remove(self):
        # A metódusnak return -1 értéket kell adnia, ha a removable_pieces üres
        result = self.player.choose_opponent_piece_to_remove(["..", ".."], [])
        self.assertEqual(result, -1)  # vagy bármilyen más érték, ami a nem eltávolítható állapotot jelzi

        # Ellenőrizzük, hogy ha van eltávolítható bábú, azt visszaadja
        result = self.player.choose_opponent_piece_to_remove(["..", ".."], [1, 2])
        self.assertIn(result, [1, 2])  # Várhatóan 1 vagy 2, ha a metódus kész van

if __name__ == "__main__":
    unittest.main()
