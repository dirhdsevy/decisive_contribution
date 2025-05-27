from Piece import Piece

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'white'
        self.white_captured = 0
        self.black_captured = 0
        self.must_capture = False
        self.last_capture_pos = None
        self.setup_pieces()

    def setup_pieces(self):
        for row in range(3):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('black', row, col)

        for row in range(5, self.size):
            for col in range(self.size):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Piece('white', row, col)

    def get_forced_captures(self, only_for_piece=None):
        captures = []
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece.color == self.current_player:
                    if only_for_piece and (row, col) != only_for_piece:
                        continue
                    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
                    for dr, dc in directions:
                        end_row = row + dr
                        end_col = col + dc
                        mid_row = row + dr // 2
                        mid_col = col + dc // 2
                        if (0 <= end_row < self.size and 0 <= end_col < self.size and
                                self.grid[end_row][end_col] is None and
                                self.grid[mid_row][mid_col] and
                                self.grid[mid_row][mid_col].color != self.current_player):
                            captures.append(((row, col), (end_row, end_col)))
        return captures

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if not (0 <= end_row < self.size and 0 <= end_col < self.size):
            return False
        if piece is None or piece.color != self.current_player:
            return False

        forced_captures = self.get_forced_captures()
        if forced_captures:
            return (start, end) in forced_captures

        if not piece.is_king:
            if piece.color == 'white' and end_row >= start_row:
                return False
            if piece.color == 'black' and end_row <= start_row:
                return False

            if abs(end_row - start_row) != 1 or abs(end_col - start_col) != 1:
                return False
        else:
            if abs(end_row - start_row) != abs(end_col - start_col):
                return False

            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            current_row, current_col = start_row + step_row, start_col + step_col

            while current_row != end_row and current_col != end_col:
                if self.grid[current_row][current_col] is not None:
                    return False
                current_row += step_row
                current_col += step_col

        if self.grid[end_row][end_col] is not None:
            return False

        return True

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.must_capture = False
        self.last_capture_pos = None

    def move_piece(self, start, end):
        if not self.is_valid_move(start, end):
            return False

        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]
        self.grid[start_row][start_col] = None
        self.grid[end_row][end_col] = piece
        piece.row, piece.col = end_row, end_col

        multi_capture_occurred = False

        if abs(start_row - end_row) >= 2:
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
            current_row, current_col = start_row + step_row, start_col + step_col
            captured_positions = []

            while current_row != end_row and current_col != end_col:
                if self.grid[current_row][current_col] is not None:
                    captured_piece = self.grid[current_row][current_col]
                    if captured_piece.color == 'white':
                        self.white_captured += 1
                    else:
                        self.black_captured += 1
                    self.grid[current_row][current_col] = None
                    captured_positions.append((current_row, current_col))
                current_row += step_row
                current_col += step_col

            if captured_positions:
                self.must_capture = True
                self.last_capture_pos = (end_row, end_col)
                if self.get_forced_captures(only_for_piece=(end_row, end_col)):
                    return True
                else:
                    self.must_capture = False
                    self.last_capture_pos = None

        if (piece.color == 'white' and end_row == 0) or \
                (piece.color == 'black' and end_row == self.size - 1):
            piece.promote_to_king()

        self.switch_player()
        return True

    def check_winner(self):
        white_exists = any(piece for row in self.grid for piece in row if piece and piece.color == "white")
        black_exists = any(piece for row in self.grid for piece in row if piece and piece.color == "black")
        if not white_exists: return "black"
        if not black_exists: return "white"
        return None


