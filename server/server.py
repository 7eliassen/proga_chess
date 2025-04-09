"""Тут будет нахоиться серверная часть приложения"""
import socket
import threading
import json
import random

def create_room(conn):
    """Здесь будет создание комнаты"""
    #TODO: Создание объекта игры
    room_id = random.randint(1000, 9999)
    #TODO: Добавить проверку коллизий id
    #TODO: Связать room_id и объект игры
    data = {'type': 's_room_id',
            'room_id': room_id}
    json_data = json.dumps(data)
    message = json_data.encode()
    conn.send(message)


def handle_client(conn, addr):
    """Отдельный поток для каждого клиента"""
    print(f"[+] Подключился {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        json_data = json.loads(data)
        type = json_data['type']
        # В зависимости от типа запроса, вызываем разные функции
        if type == 'create':
            create_room(conn)
        elif type == 'join':
            ...
        print(f"[?] [{addr}] {data}")

    conn.close()
    print(f"[-] Отключился {addr}")

def start_server(address:str, port:int) -> socket.socket:
    s = socket.socket()
    s.bind((address, port))
    s.listen(5)
    print("[*] Сервер запущен")
    return s


if __name__=="__main__":
    server = start_server('localhost', 12345)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()