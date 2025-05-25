import tkinter as tk
from tkinter import messagebox
from Board import Board
from players import AIPlayer


class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.cell_size = 60
        self.selected_piece = None

        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        self.restart_button = tk.Button(self.control_frame, text="Нова гра", command=self.restart)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.bot_button = tk.Button(self.control_frame, text="Гра з ботом", command=self.start_bot_game)
        self.bot_button.pack(side=tk.LEFT, padx=10)

        self.white_counter = tk.Label(self.control_frame, text="Знищено білих: 0")
        self.white_counter.pack(side=tk.LEFT, padx=10)

        self.black_counter = tk.Label(self.control_frame, text="Знищено чорних: 0")
        self.black_counter.pack(side=tk.LEFT, padx=10)

        self.root.title("Шашки")
        self.canvas = tk.Canvas(
            root,
            width=self.board.size * self.cell_size,
            height=self.board.size * self.cell_size
        )
        self.canvas.pack()

        self.colors = {
            "light": "#f0d9b5",
            "dark": "#b58863",
            "white_piece": "#ffffff",
            "black_piece": "#000000",
            "highlight": "#ff0000"
        }

        self.is_bot_game = False
        self.bot = None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.handle_click)

    def start_bot_game(self):
        self.is_bot_game = True
        self.bot = AIPlayer('black', self)
        self.board = Board()
        self.selected_piece = None
        self.update_counters()
        self.draw_board()
        messagebox.showinfo("Гра з ботом", "Ви граєте білими. Зробіть свій хід!")

    def restart(self):
        self.is_bot_game = False
        self.bot = None
        self.board = Board()
        self.selected_piece = None
        self.update_counters()
        self.draw_board()

    def update_counters(self):
        self.white_counter.config(text=f"Знищено білих: {self.board.white_captured}")
        self.black_counter.config(text=f"Знищено чорних: {self.board.black_captured}")

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(self.board.size):
            for col in range(self.board.size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self.colors["light"] if (row + col) % 2 == 0 else self.colors["dark"]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if self.selected_piece and (row, col) == self.selected_piece:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.colors["highlight"], width=3)

                piece = self.board.grid[row][col]
                if piece:
                    fill = self.colors["white_piece"] if piece.color == "white" else self.colors["black_piece"]
                    outline = "gray" if piece.color == "white" else "white"

                    self.canvas.create_oval(
                        x1 + 5, y1 + 5,
                        x2 - 5, y2 - 5,
                        fill=fill, outline=outline, width=2
                    )

                    if piece.is_king:
                        self.canvas.create_text(
                            (x1 + x2) // 2, (y1 + y2) // 2,
                            text="♛", font=("Arial", 20), fill="gold"
                        )

    def handle_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.is_bot_game and self.board.current_player == 'black':
            return

        if self.selected_piece is None:
            piece = self.board.grid[row][col]
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.draw_board()
        else:
            start_row, start_col = self.selected_piece
            if self.board.move_piece((start_row, start_col), (row, col)):
                self.update_counters()
                self.draw_board()

                if self.board.must_capture and self.board.last_capture_pos == (row, col):
                    self.selected_piece = (row, col)
                else:
                    self.selected_piece = None
                    if self.is_bot_game and self.board.current_player == 'black':
                        self.root.after(1000, self.bot.make_move)
            else:
                self.selected_piece = None
                self.draw_board()

        winner = self.board.check_winner()
        if winner:
            messagebox.showinfo("Гра завершена", f"Переміг гравець {winner}!")
            self.restart()


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersApp(root)
    root.mainloop()