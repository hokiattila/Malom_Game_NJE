from .player import Player

from typing import List
from typing import Tuple
from typing import Union

# HumanPlayer - emberi jatekos
# Player osztaly leszarmazottja
# Debug modban stdout-on keresztul kapja meg a userinputot,
# alapmodban GUI feluleten


class HumanPlayer(Player):

    def __init__(self: "HumanPlayer", color: str) -> None:
        super().__init__(color)
        self.name = "HumanPlayer"

    def get_valid_move(self: "HumanPlayer", valid_moves) -> Tuple[int, int]:
        pieces = {move[0] for move in valid_moves}  # Kiválasztott korongok egyedi készlete
        print(f"Available moves: {pieces}")
        # Kérjük be a korongot a felhasználótól
        piece_to_move = None
        while True:
            try:
                piece_to_move = int(input(f"Pick one of the available moves: {pieces}: "))
                if piece_to_move in pieces:
                    break  # Ha a választott korong érvényes, kilépünk a ciklusból
                else:
                    print("Invalid move, please try again.")
            except ValueError:
                print("Invalid input, please provide a valid move.")
        # Kiírjuk a kiválasztott koronghoz tartozó szomszédokat
        neighbors = [move[1] for move in valid_moves if move[0] == piece_to_move]
        print(f"{piece_to_move} neighbours: {neighbors}")
        # Kérjük be a szomszédot a felhasználótól
        neighbor_to_move = None
        while True:
            try:
                neighbor_to_move = int(input(f"Choose one neighbour piece from the following: {neighbors}: "))
                if neighbor_to_move in neighbors:
                    return (piece_to_move, neighbor_to_move)  # Visszaadjuk az érvényes lépést
                else:
                    print(f"Move {neighbor_to_move} is not a valid neighbour move! Please input another one:")
            except ValueError:
                print("Invalid input! Please provide a number.")



    def make_move(self: "HumanPlayer", valid_moves: Union[List[int], List[Tuple[int, int]]]) -> Union[int, Tuple[int, int], None]:
            # Ellenőrizzük, hogy vannak-e érvényes lépések
            if not valid_moves:
                print("There are no valid moves!")
                return None
            while True:  # Addig ismételjük, amíg nem kapunk érvényes bemenetet
                if all(isinstance(move, tuple) for move in valid_moves):
                    return self.get_valid_move(valid_moves)
                else:
                    try:
                        # Bekérjük a játékos lépését
                        move = int(input("Make a move (number between 0 and 23) "))
                        # Ellenőrizzük, hogy a megadott lépés érvényes-e
                        if move in valid_moves:
                            return move  # Ha érvényes, visszatérünk vele
                        else:
                            print(f"The move {move} is not valid! Try again.")
                    except ValueError:
                        # Ha nem sikerül a bemenetet számra konvertálni, hibát dobunk
                        print("Invalid input! Please provide a number between 0 and 23.")


    @staticmethod
    def choose_opponent_piece_to_remove(removable_pieces: List[int]) -> int:
            while True:  # Addig ismételjük, amíg nem kapunk érvényes bemenetet
                try:
                    # Bekérjük a játékos lépését
                    print("Removable pieces: " + str(removable_pieces))
                    move = int(input("Input the piece you want to remove: "))
                    # Ellenőrizzük, hogy a megadott lépés érvényes-e
                    if move in removable_pieces:
                        return move  # Ha érvényes, visszatérünk vele
                    else:
                        print(f"The move  {move} is not removable! Try again.")
                except ValueError:
                    # Ha nem sikerül a bemenetet számra konvertálni, hibát dobunk
                    print("Invalid input!")

if __name__ == "__main__":
    print("This script cannot be run directly.")