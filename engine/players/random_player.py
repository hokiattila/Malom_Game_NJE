from player import Player

class RandomPlayer(Player):

    def __init__(self, color):
        self.color = color

    def make_move(self, board):
        pass


if __name__ == '__main__':
    print("This script cannot be run directly.")