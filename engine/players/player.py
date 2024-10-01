from abc import ABC, abstractmethod

class Player(ABC):

    @abstractmethod
    def make_move(self, board):
        pass

if __name__ == '__main__':
    print("This script cannot be run directly.")