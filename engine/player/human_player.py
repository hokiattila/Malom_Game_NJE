from .player import Player

# HumanPlayer - emberi jatekos
# Player osztaly leszarmazottja
# Debug modban stdout-on keresztul kapja meg a userinputot,
# alapmodban GUI feluleten

# Milestone 1 - TODO (Armand)
class HumanPlayer(Player):

    def __init__(self, color):
        super().__init__(color)

    # Milestone 1 TODO (Armand)
    def make_move(self, board):
        pass

    # Milestone 1 TODO (Armand)
    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces):
        pass

if __name__ == "__main__":
    print("This script cannot be run directly.")