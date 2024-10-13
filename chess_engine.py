from enum import Enum
from typing import List, Union, Tuple, Optional, Dict

class WhitePieces(Enum):
    ROOK = 5
    PAWN = 1
    BISHOP = 3.5
    KNIGHT = 3
    QUEEN = 8
    KING = 0
    

class BlackPieces(Enum):
    ROOK = 5
    PAWN = 1
    BISHOP = 3.5
    KNIGHT = 3
    QUEEN = 8
    KING = 0


DEFAULT_BOARD: List[List[Optional[Union[WhitePieces, BlackPieces]]]] = [
    [BlackPieces.ROOK, BlackPieces.KNIGHT, BlackPieces.BISHOP, BlackPieces.QUEEN, BlackPieces.KING, BlackPieces.BISHOP, BlackPieces.KNIGHT, BlackPieces.ROOK],
    [BlackPieces.PAWN] * 8,
    [None] * 8,  # Empty spaces
    [None] * 8,  # Empty spaces
    [None] * 8,  # Empty spaces
    [None] * 8,  # Empty spaces
    [WhitePieces.PAWN] * 8,
    [WhitePieces.ROOK, WhitePieces.KNIGHT, WhitePieces.BISHOP, WhitePieces.QUEEN, WhitePieces.KING, WhitePieces.BISHOP, WhitePieces.KNIGHT, WhitePieces.ROOK],
]


class ChessEngine:
    def __init__(self) -> None:
        self.board: List[List[Optional[Union[WhitePieces, BlackPieces]]]] = DEFAULT_BOARD
        self.white_king_moved = False
        self.black_king_moved = False
        self.white_rook_moved = {"kingside": False, "queenside": False}
        self.black_rook_moved = {"kingside": False, "queenside": False}
        self.king_positions = {"white": (7, 4), "black": (0, 4)}  # Track the positions of the kings


    @staticmethod
    def to_algebraic(row: int, col: int) -> str:
        """Converts (row, col) coordinates into algebraic chess notation."""
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return f"{columns[col]}{8 - row}"  # 8 - row to flip the row for correct chess notation.

    def load_board(self, configuration: List[List[Optional[Union[WhitePieces, BlackPieces]]]]):
        """Loads a custom board configuration."""
        self.board = configuration

    def rules_restrictions(self, piece: Union[WhitePieces, BlackPieces], start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Defines rules for each piece. Only handles basic movement validation."""
        start_x, start_y = start
        end_x, end_y = end

        if not (0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        if piece == WhitePieces.ROOK or piece == BlackPieces.ROOK:
            return start_x == end_x or start_y == end_y

        if piece == WhitePieces.BISHOP or piece == BlackPieces.BISHOP:
            return abs(start_x - end_x) == abs(start_y - end_y)

        if piece == WhitePieces.QUEEN or piece == BlackPieces.QUEEN:
            return (start_x == end_x or start_y == end_y) or (abs(start_x - end_x) == abs(start_y - end_y))

        if piece == WhitePieces.KNIGHT or piece == BlackPieces.KNIGHT:
            return (abs(start_x - end_x), abs(start_y - end_y)) in [(1, 2), (2, 1)]

        if piece == WhitePieces.KING or piece == BlackPieces.KING:
            # Basic king movement: one square in any direction
            if max(abs(start_x - end_x), abs(start_y - end_y)) == 1:
                return True
            
            # Castling logic
            if piece == WhitePieces.KING and not self.white_king_moved:
                # Kingside castling
                if start == (7, 4) and end == (7, 6) and not self.white_rook_moved["kingside"]:
                    if self.board[7][5] is None and self.board[7][6] is None:
                        return True
                # Queenside castling
                if start == (7, 4) and end == (7, 2) and not self.white_rook_moved["queenside"]:
                    if self.board[7][1] is None and self.board[7][2] is None and self.board[7][3] is None:
                        return True
            
            if piece == BlackPieces.KING and not self.black_king_moved:
                # Kingside castling
                if start == (0, 4) and end == (0, 6) and not self.black_rook_moved["kingside"]:
                    if self.board[0][5] is None and self.board[0][6] is None:
                        return True
                # Queenside castling
                if start == (0, 4) and end == (0, 2) and not self.black_rook_moved["queenside"]:
                    if self.board[0][1] is None and self.board[0][2] is None and self.board[0][3] is None:
                        return True

        if piece == WhitePieces.PAWN:
            if start_x == 6:
                return (start_x - end_x) in [1, 2] and start_y == end_y
            return (start_x - end_x) == 1 and start_y == end_y

        if piece == BlackPieces.PAWN:
            if start_x == 1:
                return (end_x - start_x) in [1, 2] and start_y == end_y
            return (end_x - start_x) == 1 and start_y == end_y

        return False

    def get_actions(self, turn: Union[WhitePieces, BlackPieces]) -> Dict[str, List[str]]:
        """Generates a dictionary of valid actions for each piece on the board."""
        valid_moves: Dict[str, List[str]] = {}
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and isinstance(piece, type(turn)):
                    # Generate a list of valid moves for the current piece
                    piece_moves = []
                    for x in range(8):
                        for y in range(8):
                            if self.rules_restrictions(piece, (i, j), (x, y)):
                                piece_moves.append(self.to_algebraic(x, y))

                    if piece_moves:
                        # Add the piece and its moves to the dictionary
                        piece_name = f"{piece.name} at {self.to_algebraic(i, j)}"
                        valid_moves[piece_name] = piece_moves
        return valid_moves

    def is_in_check(self, color: str) -> bool:
        """Checks if the given color's king is in check."""
        king_position = self.king_positions[color]
        opponent = WhitePieces if color == "black" else BlackPieces

        # Check if any of the opponent's pieces can move to the king's position
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and isinstance(piece, type(opponent.ROOK)):
                    if self.rules_restrictions(piece, (i, j), king_position):
                        return True
        return False

    def is_checkmate(self, color: str) -> bool:
        """Checks if the given color is in checkmate."""
        if not self.is_in_check(color):
            return False

        # Get the color's pieces and see if any legal moves can be made
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and isinstance(piece, type(WhitePieces if color == "white" else BlackPieces)):
                    for x in range(8):
                        for y in range(8):
                            if self.rules_restrictions(piece, (i, j), (x, y)):
                                # Temporarily move the piece to test the move
                                saved_piece = self.board[x][y]
                                self.board[x][y], self.board[i][j] = piece, None

                                if not self.is_in_check(color):  # If the move gets the king out of check
                                    # Undo the move and return False (not checkmate)
                                    self.board[i][j], self.board[x][y] = piece, saved_piece
                                    return False

                                # Undo the move
                                self.board[i][j], self.board[x][y] = piece, saved_piece
        return True
    
    def make_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Moves a piece from the start position to the end position if valid."""
        start_x, start_y = start
        end_x, end_y = end
        piece = self.board[start_x][start_y]

        if not piece:
            print("No piece at the start position.")
            return False

        # Validate the move
        if not self.rules_restrictions(piece, start, end):
            print("Invalid move for the piece.")
            return False
        
        # Check if the destination contains a piece of the same color
        target_piece = self.board[end_x][end_y]
        if target_piece and isinstance(target_piece, type(piece)):
            print("Invalid move: You cannot place a piece on top of your own piece.")
            return False

        # Special handling for castling
        if piece == WhitePieces.KING and start == (7, 4) and end == (7, 6):  # Kingside castling
            self.board[7][5], self.board[7][7] = self.board[7][7], None  # Move the rook
            self.white_king_moved = True
            self.white_rook_moved["kingside"] = True
        elif piece == WhitePieces.KING and start == (7, 4) and end == (7, 2):  # Queenside castling
            self.board[7][3], self.board[7][0] = self.board[7][0], None  # Move the rook
            self.white_king_moved = True
            self.white_rook_moved["queenside"] = True
        elif piece == BlackPieces.KING and start == (0, 4) and end == (0, 6):  # Kingside castling
            self.board[0][5], self.board[0][7] = self.board[0][7], None  # Move the rook
            self.black_king_moved = True
            self.black_rook_moved["kingside"] = True
        elif piece == BlackPieces.KING and start == (0, 4) and end == (0, 2):  # Queenside castling
            self.board[0][3], self.board[0][0] = self.board[0][0], None  # Move the rook
            self.black_king_moved = True
            self.black_rook_moved["queenside"] = True

        # Move the king or other pieces
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = None  # Clear the start position

        # Mark the king or rook as moved
        if piece == WhitePieces.KING:
            self.white_king_moved = True
        elif piece == BlackPieces.KING:
            self.black_king_moved = True
        elif piece == WhitePieces.ROOK and start == (7, 0):  # Queenside rook
            self.white_rook_moved["queenside"] = True
        elif piece == WhitePieces.ROOK and start == (7, 7):  # Kingside rook
            self.white_rook_moved["kingside"] = True
        elif piece == BlackPieces.ROOK and start == (0, 0):  # Queenside rook
            self.black_rook_moved["queenside"] = True
        elif piece == BlackPieces.ROOK and start == (0, 7):  # Kingside rook
            self.black_rook_moved["kingside"] = True


        # Handle pawn promotion
        if piece == WhitePieces.PAWN and end_x == 0:
            self.promote_pawn(end, WhitePieces)
        elif piece == BlackPieces.PAWN and end_x == 7:
            self.promote_pawn(end, BlackPieces)


 # Check if the current player is in check after the move
        current_color = "white" if isinstance(piece, WhitePieces) else "black"
        if self.is_in_check(current_color):
            print(f"{current_color.capitalize()} is in check!")

        # Check for checkmate
        if self.is_checkmate(current_color):
            print(f"Checkmate! {current_color.capitalize()} loses.")

        return True
    

    def promote_pawn(self, position: Tuple[int, int], color: Union[WhitePieces, BlackPieces]):
        """Promotes a pawn to a different piece when it reaches the opposite end of the board."""
        print(f"Pawn at {self.to_algebraic(*position)} is eligible for promotion!")
        print("Choose a piece to promote to: (Q)ueen, (R)ook, (B)ishop, (K)night")
        choice = input().upper()

        if choice == "Q":
            self.board[position[0]][position[1]] = color.QUEEN
        elif choice == "R":
            self.board[position[0]][position[1]] = color.ROOK
        elif choice == "B":
            self.board[position[0]][position[1]] = color.BISHOP
        elif choice == "K":
            self.board[position[0]][position[1]] = color.KNIGHT
        else:
            print("Invalid choice. Defaulting to Queen.")
            self.board[position[0]][position[1]] = color.QUEEN


    def print_board(self):
        """Prints the current state of the board using algebraic notation."""
        for i, row in enumerate(self.board):
            row_display = []
            for j, piece in enumerate(row):
                if piece:
                    row_display.append(f"{piece.name}({self.to_algebraic(i, j)})")
                else:
                    row_display.append("  ")
            print(" | ".join(row_display))



# Initialize the chess engine
chess_engine = ChessEngine()
chess_engine.print_board()

# Sequence of basic moves

# 1. White Pawn e2 to e4
print("\n1. White Pawn e2 to e4")
chess_engine.make_move((6, 4), (4, 4))  # e2 to e4
chess_engine.print_board()

# 2. Black Pawn e7 to e5
print("\n2. Black Pawn e7 to e5")
chess_engine.make_move((1, 4), (3, 4))  # e7 to e5
chess_engine.print_board()

# 3. White Knight g1 to f3
print("\n3. White Knight g1 to f3")
chess_engine.make_move((7, 6), (5, 5))  # g1 to f3
chess_engine.print_board()

# 4. Black Knight b8 to c6
print("\n4. Black Knight b8 to c6")
chess_engine.make_move((0, 1), (2, 2))  # b8 to c6
chess_engine.print_board()

# 5. White Bishop f1 to c4
print("\n5. White Bishop f1 to c4")
chess_engine.make_move((7, 5), (4, 2))  # f1 to c4
chess_engine.print_board()

# 6. Black Bishop f8 to c5
print("\n6. Black Bishop f8 to c5")
chess_engine.make_move((0, 5), (3, 2))  # f8 to c5
chess_engine.print_board()

# 7. White Queen d1 to h5 (threatening checkmate)
print("\n7. White Queen d1 to h5")
chess_engine.make_move((7, 3), (4, 7))  # d1 to h5
chess_engine.print_board()

# 8. Black Pawn g7 to g6 (defending against checkmate)
print("\n8. Black Pawn g7 to g6")
chess_engine.make_move((1, 6), (3, 6))  # g7 to g6
chess_engine.print_board()

# 9. White Queen h5 to f7 (Checkmate)
print("\n9. White Queen h5 to f7 (Checkmate)")
chess_engine.make_move((4, 7), (1, 4))  # h5 to f7
chess_engine.print_board()
