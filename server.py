import socket
import threading
import pickle
from Board import Board

class CheckersServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.board = Board()
        self.lock = threading.Lock()
        self.white_taken = False
        self.black_taken = False
        self.client_colors = {}

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)
            print(f"Сервер запущено на порті {self.port}")
        except OSError as e:
            print(f"Не вдалося прив'язати порт {self.port}: {e}")
            return

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while len(self.clients) < 2:
            client_sock, addr = self.server_socket.accept()
            print(f"Підключився клієнт: {addr}")
            if self.white_taken and self.black_taken:
                client_sock.sendall(pickle.dumps({"status": "full"}))
                client_sock.close()
                continue
            self.clients.append(client_sock)
            threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True).start()

    def handle_client(self, client_sock):
        try:
            available_colors = []
            if not self.white_taken:
                available_colors.append("white")
            if not self.black_taken:
                available_colors.append("black")
            client_sock.sendall(pickle.dumps({"status": "color_choice", "colors": available_colors}))

            data = client_sock.recv(4096)
            choice = pickle.loads(data)
            color = choice["color"]

            with self.lock:
                if (color == "white" and not self.white_taken) or (color == "black" and not self.black_taken):
                    self.client_colors[client_sock] = color
                    if color == "white":
                        self.white_taken = True
                    else:
                        self.black_taken = True
                    client_sock.sendall(pickle.dumps({"status": "color_accepted", "color": color}))
                else:
                    client_sock.sendall(pickle.dumps({"status": "color_taken"}))
                    client_sock.close()
                    self.clients.remove(client_sock)
                    return

            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                move = pickle.loads(data)
                with self.lock:
                    if self.board.current_player == self.client_colors[client_sock]:
                        if self.board.move_piece(move[0], move[1]):
                            self.broadcast_move(move, client_sock)
                        else:
                            pass
                    else:
                        pass
        except Exception as e:
            print(f"Помилка з клієнтом: {e}")
        finally:
            self.disconnect_client(client_sock)

    def broadcast_move(self, move, sender_sock):
        data = pickle.dumps(move)
        for client in self.clients:
            if client != sender_sock:
                try:
                    client.sendall(data)
                except:
                    pass

    def disconnect_client(self, client_sock):
        client_sock.close()
        if client_sock in self.clients:
            self.clients.remove(client_sock)
        if client_sock in self.client_colors:
            color = self.client_colors.pop(client_sock)
            if color == "white":
                self.white_taken = False
            else:
                self.black_taken = False
        print("Клієнт відключився")

if __name__ == "__main__":
    server = CheckersServer()
    server.start()
    threading.Event().wait()