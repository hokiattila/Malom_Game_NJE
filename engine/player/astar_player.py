from engine.player.player import Player
from typing import List, Tuple, Union
import random

'''
placement startegy:
1. for placing  the first piece, choose 4,10,13 or 19
2. if opponent will complete a mill by the next move [w,w,2], then place to 2,
    blocking the mill  
3. elif self can form mill eg [b,b,2] then place piece to 2
4. if self has a mill and can move out of it to form a mill again with the same setup, 
    then move out if there are no neighbouring opponent pices that can move to the place that has been fred up
5. elif oppoent is setting up unblockable mills, 
    eg opponent has places on two intersecting mill positions[3,w,18],[3,w,5]
    if black does not block 3, then white will place to 3, creating a certain mill
6. elif opponent is not setting up unblockable mill, then stup unblockable mill for self
    eg [3,B,18],[3,4,5] palce to 4: [3,b,18],[3,b,5], if white doesnt block 3, then palce to 3
7. elif none of the above, then pick the closest neighbouring empty spot 
    with highest number of junction count (4-,3-,2 branches) and place it there
    resulting in an offensive mill setup, but not the most optimal one

move steategy:
basically the same
'''


class AStarPlayer(Player):
    def __init__(self: "AStarPlayer", color: str) -> None:
        super().__init__(color)
        self.name = "AStarPlayer"
        self.opponent_color = "B" if color == "W" else "W"
        self.pieces_placed = 0

    @staticmethod
    def is_first_move(_board: List[str], _color: str) -> bool:
        return sum(1 for i in range(24) if _board[i] == _color) == 0


    def make_move(self: "GreedyPlayer", board: List[str], valid_moves: Union[List[int], List[Tuple[int, int]]]) -> \
    Union[int, Tuple[int, int], None]:
        # Randomize move selection in case of equally strong moves
        if not valid_moves:  # If no valid moves
            print("No valid moves available!")  # Game log
            return None  # Return None

        starting_strategic_positions = (4, 10, 13, 19)

        # If it's the first move, prioritize strategic positions
        if self.is_first_move(board, self.color):
            for move in valid_moves:
                if move in starting_strategic_positions:
                    if self.pieces_placed <9: self.pieces_placed += 1
                    return move  # Return the first valid strategic move

        # we have placed the first piece
        else:
            #still in placement phase
            if self.pieces_placed < 9:
                self.pieces_placed += 1
                return self._choose_best_placement(board, valid_moves)
            #in movement phase
            else:
                return self._choose_best_move(board, valid_moves)

    def _can_prevent_unblockable_mill(self, board: List[str], valid_moves: List[int]) -> Union[int, None]:
        mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14],
            [15, 16, 17], [18, 19, 20], [21, 22, 23], [0, 9, 21], [3, 10, 18],
            [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]
        ]

        for mill in mills:
            opponent_pieces = [pos for pos in mill if board[pos] == self.opponent_color]
            empty_positions = [pos for pos in mill if board[pos] == '']

            # Check if there are two opponent pieces and one empty space
            if len(opponent_pieces) == 2 and len(empty_positions) == 1:
                block_position = empty_positions[0]

                # Check if the blocking position is a valid move
                if block_position in valid_moves:
                    return block_position  # Return the position to block the mill

        return None  # Return None if no block is possible

        pass

    def _choose_best_placement(self, board: List[str], valid_moves: List[int]) -> int:
        best_moves = []

        # First, check for a move that completes a mill
        for move in valid_moves:
            if self._would_complete_mill(board, move, self.color):
                best_moves.append(move)

        if best_moves:
            return random.choice(best_moves)  # Randomly select between equally good moves

        # Block opponent mills if possible
        for move in valid_moves:
            if self._would_complete_mill(board, move, self.opponent_color):
                best_moves.append(move)

        #check if the opponent is creating an unblockable (double) mill setup
        block_position = self._can_prevent_unblockable_mill(board, valid_moves)
        if block_position is not None:
            return block_position  # Block the opponent's mill

        #if there is no higher tier solution
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
        for (start, end) in valid_moves:
            if self._would_complete_mill_after_move(board, start, end, self.opponent_color):
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
                           not AStarPlayer._is_part_of_mill(board, piece, board[piece])]

        if non_mill_pieces:
            #put smart code here: could_complete_mill_after_removal
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
