import tkinter as tk
from tkinter import messagebox, ttk
from assets import Assets
import threading
from Board import Board
from players import AIPlayer
from server import CheckersServer
from client import NetworkCheckersClient


class CheckersApp:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.cell_size = 60
        self.selected_piece = None
        self.assets = Assets()
        self.is_bot_game = False

        self.setup_ui()

        self.is_bot_game = False
        self.white_captured = 0
        self.black_captured = 0

    def update_counters(self):
        self.white_counter.config(text=f"Знищено білих: {self.board.white_captured}")
        self.black_counter.config(text=f"Знищено чорних: {self.board.black_captured}")

    def setup_ui(self):
        self.root.title("Шашки")
        self.control_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.control_frame.pack(fill="x", padx=10, pady=5)

        self.restart_btn = ttk.Button(
            self.control_frame,
            text="Нова гра",
            style="Game.TButton",
            command=self.restart
        )
        self.restart_btn.pack(side="left", padx=5)

        self.white_counter = tk.Label(
            self.control_frame,
            text="Знищено білих: 0",
            bg="#f0f0f0",
            fg="#000000",
            font=("Verdana", 10)
        )
        self.white_counter.pack(side="left", padx=10)

        self.black_counter = tk.Label(
            self.control_frame,
            text="Знищено чорних: 0",
            bg="#f0f0f0",
            fg="#000000",
            font=("Verdana", 10)
        )
        self.black_counter.pack(side="left", padx=10)

        self.canvas = tk.Canvas(
            self.root,
            width=self.board.size * self.cell_size,
            height=self.board.size * self.cell_size,
            bg="white"
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def start_bot_game(self):
        self.is_bot_game = True
        self.bot = AIPlayer('black', self)
        messagebox.showinfo("Гра з ботом", "Ви граєте білими. Зробіть свій хід!")

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board.size):
            for col in range(self.board.size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if self.selected_piece and (row, col) == self.selected_piece:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="#ff0000", width=3)

                piece = self.board.grid[row][col]
                if piece:
                    fill = "#ffffff" if piece.color == "white" else "#000000"
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

        if hasattr(self, 'bot') and self.board.current_player == 'black':
            return

        if self.selected_piece is None:
            piece = self.board.grid[row][col]
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.draw_board()
        else:
            start_row, start_col = self.selected_piece
            if self.board.move_piece((start_row, start_col), (row, col)):
                self.white_counter.config(text=f"Знищено білих: {self.board.white_captured}")
                self.black_counter.config(text=f"Знищено чорних: {self.board.black_captured}")
                self.draw_board()

                if self.board.must_capture and self.board.last_capture_pos == (row, col):
                    self.selected_piece = (row, col)
                else:
                    self.selected_piece = None
                    if hasattr(self, 'bot') and self.board.current_player == 'black':
                        self.root.after(1000, self.bot.make_move)
            else:
                self.selected_piece = None
                self.draw_board()

        winner = self.board.check_winner()
        if winner:
            messagebox.showinfo("Гра завершена", f"Переміг гравець {winner}!")
            self.restart()

    def restart(self):
        self.board = Board()
        self.selected_piece = None
        self.white_counter.config(text="Знищено білих: 0")
        self.black_counter.config(text="Знищено чорних: 0")
        self.draw_board()
        if hasattr(self, 'bot'):
            del self.bot


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.assets = Assets()
        self.setup_styles()
        self.setup_ui()
        self.assets.play_music()

    def setup_styles(self):
        style = ttk.Style()
        style.configure(
            "Menu.TButton",
            font=("Verdana", 14),
            foreground="#000000",
            background="#e0e0e0",
            padding=10,
            width=20
        )
        style.map(
            "Menu.TButton",
            background=[("active", "#d0d0d0")],
            foreground=[("active", "#000000")]
        )
        style.configure(
            "Game.TButton",
            font=("Verdana", 10),
            foreground="#000000"
        )

    def setup_ui(self):
        self.root.title("Шашки - Головне меню")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            main_frame,
            text="ШАШКИ",
            font=("Verdana", 36, "bold"),
            bg="#f0f0f0",
            fg="#000000"
        ).pack(pady=(0, 30))

        buttons = [
            ("Гра з ботом", self.start_bot_game),
            ("Гра з другом", self.start_local_game),
            ("Гра по мережі", self.show_network_options),
            ("Вихід", self.root.quit)
        ]

        for text, command in buttons:
            btn = ttk.Button(
                main_frame,
                text=text,
                style="Menu.TButton",
                command=command
            )
            btn.pack(pady=10, ipady=5)

    def start_bot_game(self):
        self.start_game("bot")

    def start_local_game(self):
        self.start_game("local")

    def show_network_options(self):
        network_win = tk.Toplevel(self.root)
        network_win.title("Мережева гра")
        network_win.geometry("400x300")
        network_win.configure(bg="#f0f0f0")

        tk.Label(
            network_win,
            text="Оберіть режим мережевої гри:",
            font=("Verdana", 14),
            bg="#f0f0f0",
            fg="#000000"
        ).pack(pady=20)

        ttk.Button(
            network_win,
            text="Створити сервер",
            style="Menu.TButton",
            command=lambda: self.start_network_game(True)
        ).pack(pady=10)

        ttk.Button(
            network_win,
            text="Приєднатися до сервера",
            style="Menu.TButton",
            command=lambda: self.start_network_game(False)
        ).pack(pady=10)

    def start_network_game(self, is_host):
        if is_host:
            threading.Thread(target=CheckersServer().start, daemon=True).start()
            messagebox.showinfo("Сервер", "Сервер запущено на порті 9999")

        self.start_game("network", is_host)

    def start_game(self, mode, is_host=False):
        self.root.withdraw()
        game_window = tk.Toplevel(self.root)
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(game_window))

        if mode == "bot":
            game = CheckersApp(game_window)
            game.start_bot_game()
        elif mode == "network":
            if is_host:
                game = CheckersApp(game_window)
            else:
                NetworkCheckersClient(game_window)
        else:
            CheckersApp(game_window)

    def on_close(self, window):
        window.destroy()
        self.root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
