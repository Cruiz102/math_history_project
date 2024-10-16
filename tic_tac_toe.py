from typing import Union
from collections import defaultdict
from enum import Enum

class Player(Enum):
    X = 1
    O = -1

class TicTacToe:
    def __init__(self) -> None:
        # Initialize the grid as a list of None, representing empty cells.
        self.grid = [None] * 9
        self.turn = Player.X

    def reset(self):
        self.grid = [None] * 9
        self.turn = Player.X

    def get_actions(self):
        # Return available actions (empty cells)
        actions = []
        for i in range(9):
            if self.grid[i] is None:
                actions.append(i)
        print(actions)
        return actions

    def have_win(self, turn: Union[Player.O, Player.X]) -> bool:
        # Define the winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        # Check if the current player has any of the winning combinations
        for combo in winning_combinations:
            if all(self.grid[i] == turn for i in combo):
                return True
        return False

    def make_move(self, position: int):
        if self.grid[position] is None:
            self.grid[position] = self.turn
            if self.have_win(self.turn):
                print(f"Player {self.turn.name} wins!")
                self.turn = Player.O if self.turn == Player.X else Player.X
                return True  # Indicate a win
            # Switch turns
            self.turn = Player.O if self.turn == Player.X else Player.X
        else:
            print("Invalid move. Try again.")

    def print_board(self):
        # Print the current state of the board in a 3x3 grid format
        symbols = {None: ".", Player.X: "X", Player.O: "O"}
        for i in range(9):
            print(symbols[self.grid[i]], end=" ")
            if (i + 1) % 3 == 0:
                print()  # Newline after every 3rd element

    def is_draw(self):
        # Check if all cells are filled and there is no winner
        return all(self.grid[i] is not None for i in range(9)) and not self.have_win(self.turn)
    

