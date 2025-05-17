from Piece import Piece 

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'white'
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

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]

        if not (0 <= end_row < self.size and 0 <= end_col < self.size):
            return False

        if piece is None or piece.color != self.current_player:
            return False

        if abs(end_row - start_row) != 1 or abs(end_col - start_col) != 1:
            return False

        if self.grid[end_row][end_col] is not None:
            return False

        return True

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def move_piece(self, start, end):
        if not self.is_valid_move(start, end):
            return False

        start_row, start_col = start
        end_row, end_col = end

        piece = self.grid[start_row][start_col]
        self.grid[start_row][start_col] = None
        self.grid[end_row][end_col] = piece
        piece.row, piece.col = end_row, end_col

        if (piece.color == 'white' and end_row == 0) or \
            (piece.color == 'black' and end_row == self.size - 1):
                piece.promote_to_king()

        self.switch_player()
        return True
