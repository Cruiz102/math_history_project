from typing import List
import random
from tic_tac_toe import TicTacToe
from abc import ABCMeta

class MDP:
    def __init__(self) -> None:
        self.agent = RandomAgent()
        self.game = TicTacToe()

    def reset(self):
        self.game.reset()

    def play(self):
        states = self.game.grid
        actions = self.game.get_actions()
        played_action = self.agent.play(actions, states)
        
        if played_action is None:
            # Handle the case where there are no valid actions (e.g., game is over or no moves left)
            return (None, self.game.grid, True)
        
        is_finished = self.game.make_move(played_action)
        return (played_action, self.game.grid, is_finished)

class Agent(ABCMeta):
    def __init__(self):
        pass
    def play(self, actions, states):
        pass


class RandomAgent():
    def __init__(self):
        pass
    def play(self, actions: List, states: List):
        if len(actions):
            return random.choice(actions)  # Return a valid action
        else:
            return None  # No valid actions available


class DPAgent:
    def __init__(self) -> None:
        pass
    def training(self) -> None:
        pass

    def play(self, actions: List, states: List):
        pass







