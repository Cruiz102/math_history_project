from manim import *
from tic_tac_toe import TicTacToe, Player  # Assuming you have this module implemented
from agent import MDP, RandomAgent          # Assuming you have this module implemented
import time

class TicTacToeScene(Scene):
    def construct(self):
        self.simulations = 20  # Total number of simulations
        self.mdp = MDP()
        self.grid_group = VGroup()  # Initialize group to hold grid and symbols
        x_wins = 0
        o_wins = 0
        draws = 0

        # Run 20 simulations in ~5 seconds
        start_time = time.time()
        for _ in range(self.simulations):
            result = self.simulate_game()
            if result == Player.X:
                x_wins += 1
            elif result == Player.O:
                o_wins += 1
            else:
                draws += 1

            # Clear the grid for the next game
            self.clear_grid()

        # Ensure the 20 simulations take approximately 5 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time < 5:
            self.wait(5 - elapsed_time)

        # Show the results as a histogram
        self.show_histogram(x_wins, o_wins)

    def simulate_game(self):
        self.mdp.reset()  # Reset the MDP for a new game
        self.create_grid()
        result = None
        for _ in range(10):  # Maximum 9 moves in a Tic-Tac-Toe game
            action, states, is_finished = self.mdp.play()

            if action is None:
                # No more actions, assume the game is over (likely a draw)
                result = None
                break
            
            self.play_move(action, self.mdp.game.turn)
            if is_finished:
                result = self.mdp.game.turn  # Get the winner
                break
        return result

    def create_grid(self):
        # Create the tic-tac-toe grid with thicker lines
        grid_lines = [
            Line(LEFT * 2 + UP * 3, LEFT * 2 + DOWN * 3, stroke_width=6),  # Vertical left line
            Line(RIGHT * 2 + UP * 3, RIGHT * 2 + DOWN * 3, stroke_width=6),  # Vertical right line
            Line(LEFT * 5 + UP, RIGHT * 5 + UP, stroke_width=6),             # Horizontal top line
            Line(LEFT * 5 + DOWN, RIGHT * 5 + DOWN, stroke_width=6)          # Horizontal bottom line
        ]
        # Add lines to the grid group
        for line in grid_lines:
            self.grid_group.add(line)
        self.play(*[Create(line) for line in grid_lines])

    def clear_grid(self):
        # Clear all elements from the grid group (remove X and O)
        self.play(FadeOut(self.grid_group))
        self.grid_group = VGroup()  # Re-initialize the group

    def play_move(self, position, player):
        # Map positions to 3x3 grid coordinates
        positions = [
            [-4, 2], [0, 2], [4, 2],
            [-4, 0], [0, 0], [4, 0],
            [-4, -2], [0, -2], [4, -2]
        ]
        x_pos, y_pos = positions[position]
        
        if player == Player.X:
            self.draw_x(x_pos, y_pos)
        else:
            self.draw_o(x_pos, y_pos)

    def draw_x(self, x, y):
        # Create the X symbol with thicker lines
        line1 = Line(np.array([x - 1, y - 1, 0]), np.array([x + 1, y + 1, 0]), stroke_width=8, color=RED)
        line2 = Line(np.array([x - 1, y + 1, 0]), np.array([x + 1, y - 1, 0]), stroke_width=8, color=RED)
        self.play(Create(line1), Create(line2), run_time=0.25)  # Faster to meet 5-second goal
        self.grid_group.add(line1, line2)  # Add the X to the group

    def draw_o(self, x, y):
        # Create the O symbol with thicker lines
        circle = Circle(radius=1, stroke_width=8, color=BLUE).move_to(np.array([x, y, 0]))
        self.play(Create(circle), run_time=0.25)  # Faster to meet 5-second goal
        self.grid_group.add(circle)  # Add the O to the group

    def show_histogram(self, x_wins, o_wins):
        # Create a bar chart showing the number of wins for each player
        wins_data = [x_wins, o_wins]
        labels = ["X Wins", "O Wins"]

        # Bar chart with 2 bars (X wins and O wins)
        chart = BarChart(
            wins_data,
            bar_names=labels,
            y_range=[0, self.simulations, 5],  # y-axis range from 0 to number of simulations
            bar_colors=[RED, BLUE],
        )
        
        self.play(Create(chart))  # Animate the creation of the histogram
        self.wait(2)  # Hold the final frame for a while before ending the scene
