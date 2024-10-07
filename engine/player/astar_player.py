from .player import Player

class AStar(Player):

    def __init__(self, color):
        super().__init__(color)

    def make_move(self, board):
        pass

    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces):
        pass

if __name__ == "__main__":
    print("This script cannot be run directly.")