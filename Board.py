from Piece import Piece

class Board:
    def __init__(self):
        self.size = 8
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
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
