from .player import Player
from typing import List
from typing import Tuple
from typing import Union

import random


class GreedyPlayer(Player): # GreedyPlayer osztaly a Player (absztrakt) leszarmazottja
    def __init__(self, color):
        super().__init__(color)
        self.name = "GreedyPlayer"

    def make_move(self: "GreedyPlayer", board: List[str], valid_moves: Union[List[int], List[Tuple[int, int]]]) -> \
    Union[int, Tuple[int, int], None]:
        if isinstance(valid_moves[0], int): # Ha a learakasi fazisban vagyunk
            return self._choose_best_placement(board, valid_moves) # meghivjuk a legjobb poziciot visszado metodust
        else: # egyebkent mozgatasi fazisban vagyunk
            return self._choose_best_move(board, valid_moves) # meghivjuk a legjobb mozgatasert felelos metodust

    def _choose_best_placement(self, board: List[str], valid_moves: List[int]) -> int:  # a lerakasi fazist vizsgalo metodus
        best_moves = [] # letrehozunk egy tarolot az optimalis lepeseknek
        for move in valid_moves: # vegigiteralunk a valid lepeseken
            if self._would_complete_mill(board, move, self.color): # ha az adott lepesel malmunk keletkezik
                best_moves.append(move) # hozzadajuk az optimalis lepesekhez
        if best_moves: # ha az optimalis listank nem ures
            return random.choice(best_moves)  # visszadjuk az egyik lepest az optimalisak kozul
        # ha nincs ilyen
        opponent_color = 'B' if self.color == 'W' else 'W' # meghatarozzuk az ellenfel szinet
        for move in valid_moves: # vegigiteralunk a valid lepeseken
            if self._would_complete_mill(board, move, opponent_color): # ha egy adott pozicioval az ellenfelnek malma keletkezne
                best_moves.append(move) # hozzadajuk a leptest az optimalisokhoz
        if best_moves: # ha a listank nem ures
            return random.choice(best_moves)  # veletlenszeruen visszaadunk egyet az optimalis listankbol
        # ha ezek utan is ures a listank
        return random.choice(valid_moves) # visszaadunk egyet veletlenszeruen a szabalyos lepesek kozul


    def _choose_best_move(self, board: List[str], valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]: # a mozgatasi fazist vizsgalo metodus
        best_moves = [] # letrehozunk egy tarolot az optimalis lepeseknek
        for (start, end) in valid_moves: # vegigiteralunk a valid lepeseken
            if self._would_complete_mill_after_move(board, start, end, self.color): # ha a mozgatast kovetoen malmunk keletkezik
                best_moves.append((start, end)) # hozzaadjuk a lepest a listankhoz
        if best_moves: # ha az optimum listank nem ures
            return random.choice(best_moves)  # visszaadunk egyet veletlenszeruen
        # ha nincs ilyen
        opponent_color = 'B' if self.color == 'W' else 'W' # meghatarozzuk az ellenfel szinet
        for (start, end) in valid_moves: # vegigiteralunk a szabalyos lepeseken
            if self._would_complete_mill_after_move(board, start, end, opponent_color): # ha egy adott pozicioval az ellenfelnek malma keletkezne
                best_moves.append((start, end)) # hozzaadjuk a lepest az optimalisakhoz
        if best_moves: # ha az optimalis listank nem ures
            return random.choice(best_moves)  # veletlenszeruen visszaadunk egyet az optimalis lepesek kozul
        # ha ezek utan sem talaltunk optimalis lepest, vagyis ures a best_moves lista
        return random.choice(valid_moves) # veletlenszeruen visszaadunk egyet a szabalyos lepesek kozul amit a jatekmotortol kaptunk

    # Ellenorzi egy adott lepes malmot adna-e
    def _would_complete_mill(self, board: List[str], position: int, color: str) -> bool:
        # Fix malom poziciok
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]
        for mill in mills: # bejarjuk a malom kombinaciokat
            if position in mill and all(board[i] == color or i == position for i in mill): # ha a kapott pozicio malmot adna
                return True # visszaterunk igazzal
        return False # egyebkent hamissal

    # Ellenorzi egy adott mozgatas malomhoz vezetne-e
    def _would_complete_mill_after_move(self, board: List[str], start: int, end: int, color: str) -> bool:
        temp_board = board.copy() # Lemasoljuk a tabla jelenlegi allasat
        temp_board[start] = str(start)  # a kezdo mezot leuritjuk
        temp_board[end] = color  # a celmezore beirjuk a szint
        return self._would_complete_mill(temp_board, end, color) # lekerjuk, hogy igy malmot kaptunk-e

    # Visszaadja az ellenfel melyik korongjat vegyuk le
    @staticmethod
    def choose_opponent_piece_to_remove(board: List[str], removable_pieces: List[int]) -> int:
        # Lekerjuk azokat a korongokat amik nincsenek malomban
        non_mill_pieces = [piece for piece in removable_pieces if
                           not GreedyPlayer._is_part_of_mill(board, piece, board[piece])]
        if non_mill_pieces: # ha a lista nem ures
            return non_mill_pieces[0]  # levesszuk az elso korongot ami nincs malomban
        # ha ide jutunk akkor minden korong malomban van
        return removable_pieces[0] # levesszuk az elsot

    # Ellenorzi, hogy egy pozicio malomban van-e
    @staticmethod
    def _is_part_of_mill(board: List[str], position: int, color: str) -> bool:
        # Malom kombinaciok
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]
        for mill in mills: # Vegigiteralunk a kombinaciokon
            if position in mill and all(board[i] == color for i in mill): # Ha az adott pozicio malomban van
                return True # Igazat adunk vissza
        return False # Egyebkent hamisat


if __name__ == "__main__":
    print("This script cannot be run directly.")
