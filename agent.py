from typing import List
import random
from tic_tac_toe import TicTacToe
from abc import ABCMeta

class MDP:
    def __init__(self) -> None:
        self.agent = RandomAgent()
        self.game = TicTacToe()
    def play(self):
        states = self.game.grid
        actions = self.game.get_actions()
        played_action = self.agent.play(actions, states)
        is_finished = self.game.make_move(played_action)
        return (played_action, self.game.grid, is_finished)
    
    def online_learning(self):
        pass

    def offline_learning(self, iter: int):
        pass
    def observe_state(self):
        return self.game.grid


class Agent(ABCMeta):
    def __init__(self):
        pass
    def play(self, actions, states):
        pass


class RandomAgent():
    def __init__(self):
        pass
    def play(self, actions: List, states: List):
        a = random.choice(actions)
        return a


class DPAgent:
    def __init__(self) -> None:
        pass
    def training(self) -> None:
        pass

    def play(self, actions: List, states: List):
        pass







