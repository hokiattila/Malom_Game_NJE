from .player import Player
from typing import List
from typing import Tuple
from typing import Union

class GreedyPlayer(Player):

    def __init__(self, color):
        super().__init__(color)
        self.name = "GreedyPlayer"


    def make_move(self: "GreedyPlayer", valid_moves: Union[List[int], List[Tuple[int, int]]]) -> Union[int, Tuple[int, int], None]:
        pass

    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces: List[int]) -> int:
        pass

if __name__ == "__main__":
    print("This script cannot be run directly.")