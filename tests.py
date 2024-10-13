import pytest
from chess_engine import ChessEngine, WhitePieces, BlackPieces  # Assuming your chess engine is in chess_engine.py

@pytest.fixture
def engine():
    """Fixture to initialize the chess engine for each test."""
    return ChessEngine()

def test_pawn_movement(engine):
    """Test basic pawn movement."""
    # Move White Pawn from e2 to e4
    assert engine.make_move((6, 4), (4, 4))  # e2 to e4 should be valid

    # Move Black Pawn from e7 to e5
    assert engine.make_move((1, 4), (3, 4))  # e7 to e5 should be valid

def test_invalid_move_to_same_color(engine):
    """Test invalid move where a piece moves to a square occupied by the same color."""
    # Move White Pawn from e2 to e4
    assert engine.make_move((6, 4), (4, 4))  # e2 to e4 should be valid

    # Move White Knight to e4 (occupied by the same color's pawn)
    assert not engine.make_move((7, 6), (4, 4))  # Should be invalid

def test_knight_movement(engine):
    """Test Knight's legal movement."""
    # Move White Knight from g1 to f3
    assert engine.make_move((7, 6), (5, 5))  # g1 to f3 should be valid

    # Move Black Knight from b8 to c6
    assert engine.make_move((0, 1), (2, 2))  # b8 to c6 should be valid

def test_check_detection(engine):
    """Test the detection of check."""
    # Set up a scenario where the White Queen puts the Black King in check
    engine.make_move((6, 4), (4, 4))  # e2 to e4
    engine.make_move((1, 4), (3, 4))  # e7 to e5
    engine.make_move((7, 3), (3, 7))  # Queen d1 to h5 (threatening f7)

    # Move Black Pawn to block the check
    engine.make_move((1, 6), (3, 6))  # g7 to g6

    # Check if the Black King is still in check
    assert engine.is_in_check("black") == True

def test_checkmate_detection(engine):
    """Test checkmate detection with Scholar's Mate."""
    # White plays Scholar's Mate (Checkmate on move 4)
    engine.make_move((6, 4), (4, 4))  # e2 to e4
    engine.make_move((1, 4), (3, 4))  # e7 to e5
    engine.make_move((7, 6), (5, 5))  # Knight g1 to f3
    engine.make_move((0, 1), (2, 2))  # Knight b8 to c6
    engine.make_move((7, 3), (3, 7))  # Queen d1 to h5
    engine.make_move((1, 6), (3, 6))  # Black moves Pawn g7 to g6

    # White checkmates with Queen to f7
    assert engine.make_move((3, 7), (1, 4))  # Queen h5 to f7 (Checkmate)
    assert engine.is_checkmate("black") == True  # Black is checkmated

def test_castling(engine):
    """Test castling rules (kingside castling)."""
    # Make space for kingside castling
    engine.board[7][5] = None  # Empty f1
    engine.board[7][6] = None  # Empty g1
    engine.board[0][5] = None  # Empty f8
    engine.board[0][6] = None  # Empty g8

    # Test white kingside castling
    assert engine.make_move((7, 4), (7, 6))  # Castling should be valid
    assert engine.board[7][5] == WhitePieces.ROOK  # Rook should have moved to f1

    # Test black kingside castling
    assert engine.make_move((0, 4), (0, 6))  # Castling should be valid
    assert engine.board[0][5] == BlackPieces.ROOK  # Rook should have moved to f8

def test_pawn_promotion(engine):
    """Test pawn promotion to a queen."""
    # Move White Pawn from e7 to e8
    engine.board[1][4] = WhitePieces.PAWN  # Place a white pawn on e7
    assert engine.make_move((1, 4), (0, 4))  # Move it to e8

    # Simulate input choice for promotion
    engine.promote_pawn((0, 4), WhitePieces)  # Promote to Queen

    # Check if the pawn has been promoted to a queen
    assert engine.board[0][4] == WhitePieces.QUEEN

def test_illegal_castling(engine):
    """Test that castling is illegal if the king has moved."""
    # Move White King
    engine.make_move((7, 4), (6, 4))  # King moves
    engine.make_move((6, 4), (7, 4))  # King moves back

    # Now castling should be illegal
    engine.board[7][5] = None  # Empty f1
    engine.board[7][6] = None  # Empty g1

    # Attempt to castle after king has moved (should be invalid)
    assert not engine.make_move((7, 4), (7, 6))  # Castling invalid because the king moved before

def test_en_passant(engine):
    """Test en passant rule."""
    # Move White Pawn from e2 to e4
    engine.make_move((6, 4), (4, 4))

    # Move Black Pawn from d7 to d5
    engine.make_move((1, 3), (3, 3))

    # Move White Pawn from e4 to d5 (en passant)
    assert engine.make_move((4, 4), (3, 3))  # Valid en passant move

