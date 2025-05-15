import socket
import threading

class SocketClient:
    def __init__(self, gui, host='localhost', port=12345):
        self.gui = gui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.running = True

        # Запускаем поток для приёма сообщений
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    self.gui.show_message(f"Сервер: {message}")
            except:
                break

    def send(self, message):
        self.sock.sendall(message.encode('utf-8'))

    def close(self):
        self.running = False
        self.sock.close()