from typing import Union, List, Tuple
from collections import defaultdict
from enum import Enum
import copy
from dataclasses import dataclass
class Player(Enum):
    X = 1
    O = -1

@dataclass
class TicTacToeGame:
     grid: List[int]
     turn: Player



def serialize_game(game: TicTacToeGame):
     return
     
def have_win( game:TicTacToeGame ) -> bool:
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]            
        ]
        for combo in winning_combinations:
            if all(game.grid[i] == game.turn for i in combo):
                return True
        return False

def make_move(game: TicTacToeGame, position: int):
        if game.grid[position] is None:
            game.grid[position] = game.turn
            if have_win(game):
                print(f"Player {game.turn.name} wins!")
                game.turn = Player.O if game.turn == Player.X else Player.X
                return True  
            game.turn = Player.O if game.turn == Player.X else Player.X
        else:
            print("Invalid move. Try again.")

def print_board(game: TicTacToeGame):
        symbols = {None: ".", Player.X: "X", Player.O: "O"}
        for i in range(9):
            print(symbols[game.grid[i]], end=" ")
            if (i + 1) % 3 == 0:
                print()  

def is_draw(game, turn):
        return all(game.grid[i] is not None for i in range(9)) and not have_win(turn)


def state_action(state: List[int], turn: Player)-> Tuple[List[int], List[int]]:
        actions = []
        s = copy.copy(state)
        new_states = []
        for i in range(9):
            if state[i] is None:
                actions.append(i)

        for i in actions:
            s[i] = turn
            new_states.append([i for i in s])
            s[i] = None

        print(new_states)
        return  actions,new_states
    

def generate_all_tabular_states(game: TicTacToeGame):
    stack = []
    all_states = []
    stack.append(game.grid)
    while len(stack) > 0:
         curr_state = stack.pop()
         actions, states = state_action(curr_state, game.turn)
         for i in range(len(actions)):
            make_move(game, actions[i])
            stack.append(states[i])
            all_states.append(states[i])
    return all_states              

def generate_tabular_value_state(game: TicTacToeGame, turn : Player):
    pass

def generalized_policy_iteration(game: TicTacToeGame):
    pass


if __name__ == "__main__":
     game = TicTacToeGame([None]* 9, turn= Player.X)
     print(len(generate_all_tabular_states(game)))