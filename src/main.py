import copy
import random

# --- Constants for Board Representation ---
EMPTY = "__"
WHITE_PAWN = "wp"
WHITE_KING = "wk"
BLACK_PAWN = "bp"
BLACK_KING = "bk"

# --- Player Constants ---
WHITE = 0
BLACK = 1

# --- Board Dimensions ---
BOARD_SIZE = 8
ROW_CHARS = "abcdefgh"


# --- Helper Functions ---

def is_within_board(r, c):
    """Checks if given row and column are within the board boundaries."""
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def get_piece_color(piece):
    """Returns the color of a piece."""
    if piece in [WHITE_PAWN, WHITE_KING]:
        return WHITE
    elif piece in [BLACK_PAWN, BLACK_KING]:
        return BLACK
    return None  # For EMPTY or invalid piece


def is_opponent_piece(piece, current_player):
    """Checks if a piece belongs to the opponent of the current_player."""
    piece_color = get_piece_color(piece)
    if piece_color is None:
        return False
    return piece_color != current_player


def row_to_char(row_index):
    """Converts a row index (0-7) to a character (a-h)."""
    return ROW_CHARS[row_index]


def char_to_row(row_char):
    """Converts a row character (a-h) to a row index (0-7)."""
    return ROW_CHARS.find(row_char.lower())


# --- Move Class ---

class Move:
    """Represents a single move in the game."""

    def __init__(self, start_row, start_col, end_row, end_col,
                 is_capture=False, captured_piece_row=None, captured_piece_col=None):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.is_capture = is_capture
        self.captured_piece_row = captured_piece_row
        self.captured_piece_col = captured_piece_col

    def __eq__(self, other):
        """Compares two Move objects, needed to compare player entered move with all valid moves"""
        if not isinstance(other, Move):
            return NotImplemented
        return (self.start_row == other.start_row and
                self.start_col == other.start_col and
                self.end_row == other.end_row and
                self.end_col == other.end_col)

    def __hash__(self):
        """Hashes a Move object. Essential for using Move objects in sets or as dictionary keys."""
        return hash((self.start_row, self.start_col, self.end_row, self.end_col))

    def __str__(self):
        """Returns a string representation of the move using 'A0' format."""
        start_char = row_to_char(self.start_row).upper()
        end_char = row_to_char(self.end_row).upper()
        s = f"({start_char}{self.start_col})->({end_char}{self.end_col})"
        if self.is_capture:
            captured_char = row_to_char(self.captured_piece_row).upper()
            s += f" (captures {captured_char}{self.captured_piece_col})"
        return s


# --- GameState Class ---

class GameState:
    """Represents the current state of the Checkers game."""

    def __init__(self):
        self.board = self._initialize_board()
        self.current_player = BLACK  # Black always starts the game
        self.white_pieces_count = 12
        self.black_pieces_count = 12
        self.last_move_was_capture = False
        # (row, col) of the piece that just captured, if a multi-jump is possible
        self.captured_piece_position = None
        # List of Move objects for mandatory multi-jump continuations
        self.possible_multi_jump_moves = []

    def _initialize_board(self):
        """Sets up the initial checkers board."""
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Place Black pieces (top of the board, rows 0-2)
        for r in range(3):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 != 0:
                    board[r][c] = BLACK_PAWN

        # Place White pieces (bottom of the board, rows 5-7)
        for r in range(BOARD_SIZE - 3, BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 != 0:
                    board[r][c] = WHITE_PAWN
        return board

    def copy_game_state(self):
        """Returns a deep copy of the current GameState."""
        new_state = GameState()
        new_state.board = copy.deepcopy(self.board)
        new_state.current_player = self.current_player
        new_state.white_pieces_count = self.white_pieces_count
        new_state.black_pieces_count = self.black_pieces_count
        new_state.last_move_was_capture = self.last_move_was_capture
        new_state.captured_piece_position = self.captured_piece_position
        new_state.possible_multi_jump_moves = copy.deepcopy(
            self.possible_multi_jump_moves)
        return new_state

    def print_board(self):
        """Prints the current state of the board to the console."""
        print("\n   " + "  ".join(str(i) for i in range(BOARD_SIZE)))
        print("  " + "--" * BOARD_SIZE * 2)  # Adjusted for two-char piece names
        for r in range(BOARD_SIZE):
            # Print row label (a-h)
            row_char = row_to_char(r).upper()
            row_str = f"{row_char}|"
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                row_str += f" {piece}" if len(str(piece)) == 1 else f" {piece}"
            print(row_str)
        print("  " + "--" * BOARD_SIZE * 2)
        print(f"Current Player: {'WHITE' if self.current_player == WHITE else 'BLACK'}")
        print(f"White Pieces: {self.white_pieces_count}, Black Pieces: {self.black_pieces_count}")
        if self.last_move_was_capture and self.possible_multi_jump_moves:
            print(
                f"FORCED MULTI-JUMP with piece at ({row_to_char(self.captured_piece_position[0]).upper()}{self.captured_piece_position[1]})!")
            print("Possible continuations:")
            for move in self.possible_multi_jump_moves:
                print(f"  - {move}")
        print("-" * (BOARD_SIZE * 2 + 4))


# --- Core Game Logic Functions ---

def find_captures_for_piece(board, player, r, c):
    """
    Helper function to find all possible capture moves for a specific piece.
    """
    captures = []
    piece_type = board[r][c]

    if piece_type == WHITE_PAWN:
        # White pawns can only capture upside
        possible_directions = [(-1, -1), (-1, 1)]
    elif piece_type == BLACK_PAWN:
        # Black pawns can only capture downside
        possible_directions = [(1, -1), (1, 1)]
    else:
        # Kings can capture all sides
        possible_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    if piece_type == WHITE_PAWN or piece_type == BLACK_PAWN:
        for dr, dc in possible_directions:
            next_r, next_c = r + dr, c + dc
            jump_r, jump_c = r + 2 * dr, c + 2 * dc

            if is_within_board(next_r, next_c) and is_within_board(jump_r, jump_c):
                adjacent_piece = board[next_r][next_c]
                landing_square = board[jump_r][jump_c]

                if is_opponent_piece(adjacent_piece, player) and landing_square == EMPTY:
                    move = Move(r, c, jump_r, jump_c, True, next_r, next_c)
                    captures.append(move)

    elif piece_type == WHITE_KING or piece_type == BLACK_KING:
        # Kings can capture in all four diagonal directions
        for dr, dc in possible_directions:
            next_r, next_c = r + dr, c + dc
            jump_r, jump_c = r + 2 * dr, c + 2 * dc

            if is_within_board(next_r, next_c) and is_within_board(jump_r, jump_c):
                adjacent_piece = board[next_r][next_c]
                landing_square = board[jump_r][jump_c]

                if is_opponent_piece(adjacent_piece, player) and landing_square == EMPTY:
                    move = Move(r, c, jump_r, jump_c, True, next_r, next_c)
                    captures.append(move)
    return captures


def get_valid_moves(game_state: GameState, player: int, check_only_existence: bool = False) -> list[Move] | bool:
    """
    Determines all valid moves for the specified player from the current game state.
    If check_only_existence is True, returns True if any legal move exists, False otherwise.
    """
    # Check for mandatory multi-jump continuation
    if game_state.last_move_was_capture and game_state.possible_multi_jump_moves:
        if check_only_existence:
            return True
        return game_state.possible_multi_jump_moves

    # If not just checking existence, prepare sets for full list
    if not check_only_existence:
        all_potential_moves = set()
        capture_moves = set()

    # Iterate through the board to find all possible moves
    found_any_capture_on_board = False

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            current_piece = game_state.board[r][c]

            # Check if the piece belongs to the current Player
            if get_piece_color(current_piece) == player:
                current_piece_captures = find_captures_for_piece(game_state.board, player, r, c)

                if current_piece_captures:
                    found_any_capture_on_board = True
                    if check_only_existence:
                        return True
                    else:
                        capture_moves.update(current_piece_captures)

                if not current_piece_captures:
                    # Get normal moves for the current piece (non capture moves)
                    move_directions = []

                    if current_piece == WHITE_PAWN:
                        move_directions = [(-1, -1), (-1, 1)]
                    elif current_piece == BLACK_PAWN:
                        move_directions = [(1, -1), (1, 1)]
                    elif current_piece == WHITE_KING or current_piece == BLACK_KING:
                        move_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

                    for dr, dc in move_directions:
                        next_r, next_c = r + dr, c + dc
                        if is_within_board(next_r, next_c) and game_state.board[next_r][next_c] == EMPTY:
                            if check_only_existence and not found_any_capture_on_board:
                                return True

                            # Only add to set if we need the full list
                            if not check_only_existence:
                                move = Move(r, c, next_r, next_c, False)
                                all_potential_moves.add(move)

    # Enforce Mandatory Capture Rule / Final Return
    if check_only_existence:
        return False

    # If check_only_existence is False, return the actual list
    if capture_moves:
        return list(capture_moves)
    else:
        return list(all_potential_moves)


def apply_move(game_state: GameState, move: Move) -> GameState:
    """
    Applies a given move to a deep copy of the GameState and returns the new state.
    Handles piece movement, capture, king promotion, and multi-jump logic.
    """
    new_state = game_state.copy_game_state()

    # Get piece type from starting position
    piece_type = new_state.board[move.start_row][move.start_col]

    # Move the piece
    new_state.board[move.end_row][move.end_col] = piece_type
    new_state.board[move.start_row][move.start_col] = EMPTY

    # Handle capture
    if move.is_capture:
        new_state.board[move.captured_piece_row][move.captured_piece_col] = EMPTY
        if get_piece_color(piece_type) == WHITE:
            new_state.black_pieces_count -= 1
        else:
            new_state.white_pieces_count -= 1
        new_state.last_move_was_capture = True
        new_state.captured_piece_position = (move.end_row, move.end_col)
    else:
        new_state.last_move_was_capture = False
        new_state.captured_piece_position = None  # Reset if no capture

    # Handle king promotion
    if piece_type == WHITE_PAWN and move.end_row == 0:
        new_state.board[move.end_row][move.end_col] = WHITE_KING
    elif piece_type == BLACK_PAWN and move.end_row == BOARD_SIZE - 1:
        new_state.board[move.end_row][move.end_col] = BLACK_KING

    # --- Determine next turn based on multi-jump rules ---
    if new_state.last_move_was_capture:
        # Check for further captures from the *new position* of the capturing piece
        potential_next_jumps = find_captures_for_piece(
            new_state.board,
            new_state.current_player,
            new_state.captured_piece_position[0],
            new_state.captured_piece_position[1]
        )

        if potential_next_jumps:
            # Multi-jump sequence continues, current player does not change
            new_state.possible_multi_jump_moves = potential_next_jumps
            # The current_player remains the same
        else:
            # No further jumps, multi-jump sequence ends, turn passes
            new_state.possible_multi_jump_moves = []
            new_state.current_player = BLACK if new_state.current_player == WHITE else WHITE
    else:
        # No capture, turn passes normally
        new_state.possible_multi_jump_moves = []
        new_state.current_player = BLACK if new_state.current_player == WHITE else WHITE

    return new_state


def is_valid_move(game_state: GameState, move_input_str: str) -> Move | None:
    """
    Checks if provided move is valid.
    """
    try:
        parts = move_input_str.strip().split('->')

        start_coords_str = parts[0].strip()
        start_row_char = start_coords_str[0]
        start_col_str = start_coords_str[1:]
        start_row = char_to_row(start_row_char)
        start_col = int(start_col_str)

        end_coords_str = parts[1].strip()
        end_r_char = end_coords_str[0]
        end_c_str = end_coords_str[1:]
        end_r = char_to_row(end_r_char)
        end_c = int(end_c_str)

        if not (is_within_board(start_row, start_col) and is_within_board(end_r, end_c)):
            return None

        input_move = Move(start_row, start_col, end_r, end_c)

        # Get all truly valid moves for the current player
        valid_moves = get_valid_moves(game_state, game_state.current_player)

        # Check if the input move matches any of the valid moves
        for valid_move in valid_moves:
            if input_move == valid_move:
                return valid_move
        return None

    except (ValueError, IndexError):
        return None  # Invalid input format


def is_game_over(game_state: GameState) -> tuple[bool, int | None]:
    """Checks if the game has ended."""
    # Black winning condition
    if game_state.white_pieces_count == 0:
        return True, BLACK
    # White winning condition
    if game_state.black_pieces_count == 0:
        return True, WHITE

    # Check if current player has any valid moves left, if not then opponent wins
    if not get_valid_moves(game_state, game_state.current_player):
        return True, (
            BLACK if game_state.current_player == WHITE else WHITE)

    return False, None


# --- Computer Move ---

def get_computer_move(game_state: GameState, player: int) -> Move | None:
    """
    selects a random valid move for the computer player. Capturing is enforeced here as well
    """
    valid_moves = get_valid_moves(game_state, player)
    if valid_moves:
        return random.choice(valid_moves)
    return None


# --- Main Game Loop (Player vs Computer) ---

def main():
    game = GameState()

    print("--- Welcome!! Checkers Game: Player (WHITE) vs. Computer (BLACK) ---")
    print("Input moves should be in format: Row letter, Column number -> Row letter, Column number")
    print("Example: A0->C2")

    while True:
        game.print_board()
        game_over, winner = is_game_over(game)

        if game_over:
            if winner == WHITE:
                print("Game Over! WHITE (Player) wins!")
            elif winner == BLACK:
                print("Game Over! BLACK (Computer) wins!")
            else:
                print("Game Over! It's a Draw!")
            break

        if game.current_player == WHITE:
            print("Player (WHITE)'s Turn...")
            valid_input = False
            while not valid_input:
                move_str = input("Enter your move: ")
                player_move = is_valid_move(game, move_str)
                if player_move:
                    print(f"Player move: {player_move}")
                    game = apply_move(game, player_move)
                    valid_input = True
                else:
                    print("Invalid move. Please try again.")
        else:
            print("Computer (BLACK)'s Turn...")
            computer_move = get_computer_move(game, BLACK)
            if computer_move:
                print(f"Computer move: {computer_move}")
                game = apply_move(game, computer_move)
            else:
                print("Computer has no valid moves. Player (WHITE) wins!")
                break


if __name__ == "__main__":
    main()
