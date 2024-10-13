from manim import *
from tic_tac_toe import TicTacToe, Player
from agent import MDP, RandomAgent
class TicTacToeScene(Scene):
    def construct(self):
        self.mdp = MDP()
        self.create_grid()
        for i in range(10):
            action, states, is_finished = self.mdp.play()
            self.play_move(action,self.mdp.game.turn)
            if is_finished:
                break

    def create_grid(self):
        # Create the tic-tac-toe grid
        grid_lines = [
            Line(LEFT * 2 + UP*3, LEFT * 2 + DOWN*3),
            Line(LEFT, RIGHT),
            Line(RIGHT * 2 + UP*3, RIGHT * 2 + DOWN*3),
            Line(LEFT * 5 + DOWN, RIGHT * 5 + DOWN)
        ]
        # Animating grid
        self.play(*[Create(line) for line in grid_lines])

    def play_move(self, position, player):
        # Map positions to 3x3 grid coordinates
        positions = [
            [-3, 3], [0, 3], [3, 3],
            [-3, 0], [0, 0], [3, 0],
            [-3, -3], [0, -3], [3, -3]
        ]
        x_pos, y_pos = positions[position]
        
        if player == Player.X:
            self.draw_x(x_pos, y_pos)
        else:
            self.draw_o(x_pos, y_pos)

    def draw_x(self, x, y):
        # Create the X symbol
        line1 = Line(np.array([x - 1, y - 1, 0]), np.array([x + 1, y + 1, 0]))
        line2 = Line(np.array([x - 1, y + 1, 0]), np.array([x + 1, y - 1, 0]))
        self.play(Create(line1), Create(line2))

    def draw_o(self, x, y):
        # Create the O symbol
        circle = Circle(radius=1).move_to(np.array([x, y, 0]))
        self.play(Create(circle))






