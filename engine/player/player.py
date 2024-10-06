from abc import ABC, abstractmethod

# Player absztrakt osztaly
# A leszarmazottak kotelezo elemeit adja meg
class Player(ABC):

    def __init__(self, color):
        self.color = color


    @abstractmethod
    def make_move(self, board):
        pass

    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces):
        pass

if __name__ == '__main__':
    print("This script cannot be run directly.")