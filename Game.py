import tkinter as tk
from Board import Board

class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.draw_board()