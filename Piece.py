class Piece:
    def init(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.is_king = False

    def promote_to_king(self):
        self.is_king = True