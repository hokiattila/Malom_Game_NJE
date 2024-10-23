from .player import Player
from typing import List
from typing import Tuple
from typing import Union

import random


class GreedyPlayer(Player):
    def __init__(self, color):
        super().__init__(color)
        self.name = "GreedyPlayer"

    def make_move(self: "GreedyPlayer", board: List[str], valid_moves: Union[List[int], List[Tuple[int, int]]]) -> \
    Union[int, Tuple[int, int], None]:
        # Randomize move selection in case of equally strong moves
        if isinstance(valid_moves[0], int):
            # Placement Phase
            return self._choose_best_placement(board, valid_moves)
        else:
            # Movement Phase
            return self._choose_best_move(board, valid_moves)

    def _choose_best_placement(self, board: List[str], valid_moves: List[int]) -> int:
        best_moves = []

        # First, check for a move that completes a mill
        for move in valid_moves:
            if self._would_complete_mill(board, move, self.color):
                best_moves.append(move)

        if best_moves:
            return random.choice(best_moves)  # Randomly select between equally good moves

        # Block opponent mills if possible
        opponent_color = 'B' if self.color == 'W' else 'W'
        for move in valid_moves:
            if self._would_complete_mill(board, move, opponent_color):
                best_moves.append(move)

        if best_moves:
            return random.choice(best_moves)  # Randomly select between equally good moves

        # Otherwise, choose a random move from valid moves
        return random.choice(valid_moves)

    def _choose_best_move(self, board: List[str], valid_moves: List[Tuple[int, int]]) -> Tuple[int, int]:
        best_moves = []

        # First, check for a move that completes a mill
        for (start, end) in valid_moves:
            if self._would_complete_mill_after_move(board, start, end, self.color):
                best_moves.append((start, end))

        if best_moves:
            return random.choice(best_moves)  # Randomly select between equally good moves

        # Block opponent mills if possible
        opponent_color = 'B' if self.color == 'W' else 'W'
        for (start, end) in valid_moves:
            if self._would_complete_mill_after_move(board, start, end, opponent_color):
                best_moves.append((start, end))

        if best_moves:
            return random.choice(best_moves)  # Randomly select between equally good moves

        # Otherwise, return a random valid move
        return random.choice(valid_moves)

    def _would_complete_mill(self, board: List[str], position: int, color: str) -> bool:
        # Check if placing a piece at 'position' will complete a mill for 'color'
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]

        for mill in mills:
            if position in mill and all(board[i] == color or i == position for i in mill):
                return True
        return False

    def _would_complete_mill_after_move(self, board: List[str], start: int, end: int, color: str) -> bool:
        # Temporarily move the piece and check if it would form a mill
        temp_board = board.copy()
        temp_board[start] = str(start)  # Empty the start position
        temp_board[end] = color  # Move piece to end position
        return self._would_complete_mill(temp_board, end, color)

    @staticmethod
    def choose_opponent_piece_to_remove(board: List[str], removable_pieces: List[int]) -> int:
        # Try to remove a piece that is not part of a mill
        non_mill_pieces = [piece for piece in removable_pieces if
                           not GreedyPlayer._is_part_of_mill(board, piece, board[piece])]

        if non_mill_pieces:
            return non_mill_pieces[0]  # Remove the first piece not in a mill

        # If all pieces are part of mills, remove the first available piece
        return removable_pieces[0]

    @staticmethod
    def _is_part_of_mill(board: List[str], position: int, color: str) -> bool:
        # Check if a piece at 'position' is part of a mill
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]

        for mill in mills:
            if position in mill and all(board[i] == color for i in mill):
                return True
        return False


if __name__ == "__main__":
    print("This script cannot be run directly.")
