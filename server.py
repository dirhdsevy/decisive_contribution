import socket
import threading
import pickle

from Board import Board

class CheckersServer:
    def __init__(self, host='0.0.0.0', port=25565):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.board = Board()
        self.lock = threading.Lock()

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
            self.clients.append(client_sock)
            threading.Thread(target=self.handle_client, args=(client_sock,), daemon=True).start()

    def handle_client(self, client_sock):
        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                move = pickle.loads(data)
                with self.lock:
                    if self.board.move_piece(move[0], move[1]):
                        self.board.switch_player()
                        self.broadcast_move(move, client_sock)
        except Exception as e:
            print(f"Помилка з клієнтом: {e}")
        finally:
            client_sock.close()
            if client_sock in self.clients:
                self.clients.remove(client_sock)
            print("Клієнт відключився")

    def broadcast_move(self, move, sender_sock):
        data = pickle.dumps(move)
        for client in self.clients:
            if client != sender_sock:
                try:
                    client.sendall(data)
                except:
                    pass

if __name__ == "__main__":
    server = CheckersServer()
    server.start()
    threading.Event().wait()
