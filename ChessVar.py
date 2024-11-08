# Author: Audrey Do
# GitHub username: a3ry0
# Date: 06/05/24
# Description: The program implements the Atomic Chess game. It has a class, ChessVar, which handles initializing the board, managing turns, validating moves, and updating the board state. There are special rules of Atomic Chess such as handling explosions when pieces are captured which are incorporated into the move validation and execution processes. The program ensures that the game state is always up to date and has methods to determine the current state including whether the game is ongoing or if a player has won. Additionally, it includes functions to print the current board state.

class ChessVar:
    """ Represents Atomic Chess """
    def __init__(self):
        """
        Initializes chess board, sets the initial turn, and sets game state
        - 'r'/'R': rook (black/white)
        - 'n'/'N': knight (black/white)
        - 'b'/'B': bishop (black/white)
        - 'q'/'Q': queen (black/white)
        - 'k'/'K': king (black/white)
        - 'p'/'P': pawn (black/white)
        - ' ' : empty square
        """
        # board set up
        self._board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self._current_turn = 'W'  # White starts first
        self._game_state = 'UNFINISHED'  # Game state will be 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def make_move(self, start_square, next_square):
        """
        Attempt to make a move from start_square to next_pos
        Param:  start_square (str) starting position
                next_square (str)
        Returns: True if the move was successful, False if not (bool)
        """
        if self._game_state != 'UNFINISHED':
            # If game is won no more moves made
            return False

        # Convert positions to board indices
        start_row, start_col = self._convert_square_to_indices(start_square)
        next_row, to_col = self._convert_square_to_indices(next_square)

        # Check if the square is within the bounds of board
        if not (0 <= next_row < 8 and 0 <= to_col < 8):
            return False

        piece = self._board[start_row][start_col] # Get piece at starting position

        if not piece or (piece.islower() and self._current_turn == 'W') or (
                piece.isupper() and self._current_turn == 'B'):
            # If the piece does not belong to the current player
            return False

        if self._is_valid_move(piece, start_row, start_col, next_row, to_col):
            captured_piece = self._board[next_row][to_col] # capture piece at target pos if there is any
            self._board[next_row][to_col] = piece          # move piece to new pos
            self._board[start_row][start_col] = ' '        # empty starting pos

            # handles piece captures and explosions
            if captured_piece != ' ':
                if captured_piece.lower() == 'k' or piece.lower() == 'k':
                    self._game_state = 'WHITE_WON' if captured_piece.lower() == 'k' else 'BLACK_WON'
                self._explosion(next_row, to_col)

            # update the turn if game is still going
            if self._game_state == 'UNFINISHED':
                self._current_turn = 'B' if self._current_turn == 'W' else 'W'
            return True
        return False

    def print_board(self):
        """Print current state of board"""
        for row in self._board:
            print(" ".join(row))
        print()

    def _convert_square_to_indices(self, square):
        """Convert algebraic notation to board indices"""
        column, row = square # Split the input into column letters and row numbers
        return 8 - int(row), ord(column) - ord('a')

    def _is_valid_move(self, piece, start_row, start_col, next_row, next_col):
        """
        Check if move is valid with Atomic Chess rules
        Param: piece (str), piece (str), start_row (int): current row, start_col (int): current column, next_row (int): new target row, next_col (int): new target column
        Returns: True if the move is valid and False if not (bool)
        """
        if piece.lower() == 'k': # King
            # Checks if the king is moving one square in any direction
            if abs(start_row - next_row) <= 1 and abs(start_col - next_col) <= 1:
                return self._board[next_row][next_col] == ' ' or self._board[next_row][next_col].islower() != piece.islower()
            return False

        if piece.lower() == 'p': # Pawn
            if start_col == next_col: # Check if pawn is moving forward
                # White pawns decrease row number by 1
                # Black pawns increase row number by 1
                if (self._current_turn == 'W' and start_row - next_row == 1) or (self._current_turn == 'B' and next_row - start_row == 1):
                    return self._board[next_row][next_col] == ' '
                # Check if the pawn is making the first move and moving 2 squares forward
                # White pawns start row is 6 and next row is 4
                # Black pawns start row is 1 and next row is 3
                if (self._current_turn == 'W' and start_row == 6 and next_row == 4) or (self._current_turn == 'B' and start_row == 1 and next_row == 3):
                    # Start squares and square it jumps over has to be empty
                    return self._board[next_row][next_col] == ' ' and self._board[(start_row + next_row) // 2][next_col] == ' '
            # Checks if the pawn is captured diagonally
            # Must move one column left or right and move one row forward
            elif abs(start_col - next_col) == 1 and ((self._current_turn == 'W' and start_row - next_row == 1) or (self._current_turn == 'B' and next_row - start_row == 1)):
                # Must contain an opponent's piece
                return self._board[next_row][next_col] != ' ' and self._board[next_row][next_col].islower() != piece.islower()
            return False

        if piece.lower() == 'r': # Rook
            if start_row != next_row and start_col != next_col:
                return False  # Rook can only move along ranks or files
            # Iterates over columns if there are any pieces in the way
            if start_row == next_row:  # Horizontal move
                step = 1 if start_col < next_col else -1
                for col in range(start_col + step, next_col, step):
                    if not 0 <= col < 8 or self._board[start_row][col] != ' ':
                        return False
            else:  # Vertical move
                step = 1 if start_row < next_row else -1
                for row in range(start_row + step, next_row, step):
                    if not 0 <= row < 8 or self._board[row][start_col] != ' ':
                        return False
            return self._board[next_row][next_col] == ' ' or self._board[next_row][next_col].islower() != piece.islower()

        if piece.lower() == 'n': # Knight
            # Calculate absolute difference between start and next
            row_diff = abs(next_row - start_row)
            col_diff = abs(next_col - start_col)
            # Checks if knight is moving one square vertically and two squares horizontally or vice versa
            # Checks if square is empty or if square contains an opponents piece
            return (row_diff == 1 and col_diff == 2) or (row_diff == 2 and col_diff == 1) and (
                    self._board[next_row][next_col] == ' ' or self._board[next_row][next_col].islower() != piece.islower())

        if piece.lower() == 'b': # Bishop
            if abs(start_row - next_row) != abs(start_col - next_col):
                return False  # Bishop can only move diagonally
            # Determine direction of movement
            row_step = 1 if start_row < next_row else -1
            col_step = 1 if start_col < next_col else -1
            row, col = start_row + row_step, start_col + col_step
            # Iterate over each square in diagonal path
            while row != next_row:
                if self._board[row][col] != ' ':
                    return False
                row += row_step
                col += col_step
            return self._board[next_row][next_col] == ' ' or self._board[next_row][next_col].islower() != piece.islower()

        if piece.lower() == 'q': # Queen
            if start_row == next_row:  # Horizontal move
                step = 1 if start_col < next_col else -1
                for col in range(start_col + step, next_col, step):
                    if self._board[start_row][col] != ' ':
                        return False
            elif start_col == next_col:  # Vertical move
                step = 1 if start_row < next_row else -1
                for row in range(start_row + step, next_row, step):
                    if self._board[row][start_col] != ' ':
                        return False
            elif abs(start_row - next_row) == abs(start_col - next_col):  # Diagonal move
                row_step = 1 if start_row < next_row else -1
                col_step = 1 if start_col < next_col else -1
                row, col = start_row + row_step, start_col + col_step
                while row != next_row:
                    if self._board[row][col] != ' ':
                        return False
                    row += row_step
                    col += col_step
            else:
                return False
            return self._board[next_row][next_col] == ' ' or self._board[next_row][next_col].islower() != piece.islower()
            # If piece is not recognized, assume invalid move

    def _explosion(self, row, col):
        """
        Enables the explosion effect when a piece is captured.
        All pieces in a 3x3 area centered on the captured piece are removed except pawns.
        If a king is in the explosion, the game is won by the opponent.
        Param: row (int), col (int)
        """
        # Loop through 3x3 area around the captured piece
        for i in range(max(0, row - 1), min(8, row + 2)):
            for j in range(max(0, col - 1), min(8, col + 2)):
                if self._board[i][j].lower() != 'p':  # Only pawns are immune to explosion
                    if self._board[i][j].lower() == 'k':
                        self._game_state = 'BLACK_WON' if self._board[i][j] == 'K' else 'WHITE_WON'
                    self._board[i][j] = ' ' # Remove the piece from board
