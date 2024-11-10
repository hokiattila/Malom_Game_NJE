import unittest
from player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("W")  # A Player osztályt nem lehet közvetlenül példányosítani, így ezt ki kell hagyni

    def test_player_initialization(self):
        self.assertEqual(self.player.color, "W")
        self.assertEqual(str(self.player), "(White) - Player")

    def test_make_move_is_abstract(self):
        # Itt ellenőrizzük, hogy a make_move metódus valóban absztrakt-e
        with self.assertRaises(TypeError):
            Player.make_move(self.player, [], [])  # Hívja meg az absztrakt metódust, ami hibát kell okozzon

if __name__ == "__main__":
    unittest.main()