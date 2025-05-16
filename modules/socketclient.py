import socket
import threading
import json


class SocketClient:
    def __init__(self, gui, queue_, host='localhost', port=12345):
        self.gui = gui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.host = host
        self.port = port
        self.queue = queue_

    def connect_to_room(self, room):
        ...

    def create_room(self, name="TEST"):
        client = self.sock
        data = {'type': 'create',
                'name': name}
        json_str = json.dumps(data)
        self.send(json_str)


    def try_connect(self):
        try:
            self.sock.connect((self.host, self.port))
            self.running = True
            return True
        except:
            return False

    def start_loop(self):
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message:
                    self.queue.put(message)
                    print(list(self.queue))
            except:
                break

    def send(self, message):
        self.sock.sendall(message.encode('utf-8'))

    def close(self):
        self.running = False
        self.sock.close()
