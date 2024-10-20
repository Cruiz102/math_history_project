import pytest
from tic_tac_toe import TicTacToe, state_action

@pytest.fixture
def game():
    """Fixture to initialize the chess engine for each test."""
    return TicTacToe()

def x_win(game):
    """Test basic pawn movement."""
    assert game.make_move((6, 4), (4, 4))  # e2 to e4 should be valid

    assert game.make_move((1, 4), (3, 4))  # e7 to e5 should be valid

def o_win(game):
    pass

def draw(game):
    pass

def invalid_move(game):
    assert game.make_move((6, 4), (4, 4))  # e2 to e4 should be valid

    assert not game.make_move((7, 6), (4, 4))  # Should be invalid


def 