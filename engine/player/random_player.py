
from .player import Player
from typing import Union
from typing import List
from typing import Tuple
import random

# RandomPlayer profil
# Player osztaly leszarmazottja, minden korben veletlenszeruen lep
class RandomPlayer(Player):

    def __init__(self: "RandomPlayer", color: str) -> None:
       super().__init__(color)
       self.name = "RandomPlayer"


    # Veletlenszeruen valaszt egy ervenyes lepest a Game osztaly altal biztositott lepesek kozul
    # Kezeli a lerakasi es mozgatasi fazist is
    def make_move(self: "RandomPlayer",board: List[str], valid_moves: Union[List[int], List[Tuple[int, int]]]) -> Union[int, Tuple[int, int], None]:
        if not valid_moves: # Ha nincsenek ervenyes lepesek
            print("No valid moves available!")  # Game log
            return None # None-t adunk vissza
        return random.choice(valid_moves)


    # Veletlenszeruen valaszt egy eltavolitando korongot az ellenfel korongjai kozul
    # A korongok listajat a Game osztaly biztositja
    @staticmethod
    def choose_opponent_piece_to_remove(board: List[str], removable_pieces: List[int]) -> int:
            return random.choice(removable_pieces)

if __name__ == '__main__':
    print("This script cannot be run directly.")