from abc import ABC, abstractmethod
from typing import List
from typing import Tuple
from typing import Union

# Player absztrakt osztaly
# A leszarmazottak kotelezo elemeit adja meg
class Player(ABC):

    def __init__(self:"Player", color: str) -> None:
        self.color = color
        self.name = "Player"

    @abstractmethod
    def make_move(self: "Player",board: List[str], valid_moves: Union[List[int], List[Tuple[int, int]]]) -> Union[int, Tuple[int, int], None]:
        pass


    @staticmethod
    def choose_opponent_piece_to_remove(board: List[str], removable_pieces: List[int]):
        pass

    def __str__(self: "Player") -> str:
        return f"({"White" if self.color == "W" else "Black"}) - {self.name}"

if __name__ == '__main__':
    print("This script cannot be run directly.")