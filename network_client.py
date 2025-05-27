import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
import pickle
from Board import Board


class NetworkCheckersClient:
    def __init__(self, root):
        self.root = root
        self.board = Board()
        self.cell_size = 60
        self.selected_piece = None
        self.sock = None
        self.connected = False
        self.my_color = None

        self.root.title("Мережева гра в шашки")
        self.canvas = tk.Canvas(root, width=self.board.size * self.cell_size,
                                height=self.board.size * self.cell_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)
        self.draw_board()
        self.connect_to_server()

    def connect_to_server(self):
        ip = simpledialog.askstring("IP сервера", "Введіть IP-адресу сервера:")
        if not ip:
            self.root.destroy()
            return

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, 9999))
            self.connected = True
            data = self.sock.recv(4096)
            message = pickle.loads(data)

            if message["status"] == "full":
                messagebox.showerror("Помилка", "Гра вже має двох гравців.")
                self.root.destroy()
                return
            elif message["status"] == "color_choice":
                available_colors = message["colors"]
                if len(available_colors) == 1:
                    self.my_color = available_colors[0]
                    messagebox.showinfo("Колір призначено", f"Вам призначено колір: {self.my_color}")
                else:
                    self.my_color = self.choose_color(available_colors)

                self.sock.sendall(pickle.dumps({"color": self.my_color}))
                data = self.sock.recv(4096)
                response = pickle.loads(data)

                if response["status"] == "color_accepted":
                    self.my_color = response["color"]
                    messagebox.showinfo("Підключено", f"Ви граєте за {self.my_color}.")
                    threading.Thread(target=self.listen_to_server, daemon=True).start()
                else:
                    messagebox.showerror("Помилка", "Вибраний колір вже зайнятий.")
                    self.root.destroy()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося підключитись: {e}")
            self.root.destroy()

    def choose_color(self, available_colors):
        color_choice = simpledialog.askstring("Вибір кольору", f"Оберіть колір ({', '.join(available_colors)}):")
        while color_choice not in available_colors:
            color_choice = simpledialog.askstring("Вибір кольору",
                                                  f"Невірний вибір. Оберіть колір ({', '.join(available_colors)}):")
        return color_choice

    def listen_to_server(self):
        while self.connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                move = pickle.loads(data)
                self.board.move_piece(move[0], move[1])
                self.draw_board()
            except Exception as e:
                print("Помилка з'єднання:", e)
                break

    def handle_click(self, event):
        if self.board.current_player != self.my_color:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_piece is None:
            piece = self.board.grid[row][col]
            if piece and piece.color == self.my_color:
                self.selected_piece = (row, col)
        else:
            start = self.selected_piece
            end = (row, col)
            if self.board.move_piece(start, end):
                self.send_move(start, end)
                self.selected_piece = None
                self.draw_board()
            else:
                self.selected_piece = None

    def send_move(self, start, end):
        if self.sock:
            try:
                data = pickle.dumps((start, end))
                self.sock.sendall(data)
            except:
                pass

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board.size):
            for col in range(self.board.size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board.grid[row][col]
                if piece:
                    fill = "#ffffff" if piece.color == "white" else "#000000"
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=fill, width=2)
                    if piece.is_king:
                        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="♛", font=("Arial", 20),
                                                fill="gold")

