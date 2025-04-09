"""Тут будет нахоиться серверная часть приложения"""
# TODO: добавить логирование
import socket
import threading
import json
import random
import modules.game as game

#FIXME: временно
# room_id: [game, who_wait]
games = {}


def create_room(conn):
    """Здесь будет создание комнаты"""
    new_game = game

    #TODO: модифицировать проверку на коллизии
    room_id = random.randint(1000, 9999)
    while room_id in games.keys():
        room_id = random.randint(1000, 9999)

    games[room_id] = [new_game, conn]
    data = {'type': 's_room_id',
            'room_id': room_id}
    json_data = json.dumps(data)
    message = json_data.encode()
    conn.send(message)
    print(f'[+] Создана комната {room_id}')

def join_room(conn, room_id):
    #FIXME: Создать настоящее присоединение к комнате
    if room_id in games.keys():
        game, conn2 = games[room_id]
        #FIXME: Отправка данных по JSON
        conn2.send(b"opponent is found")
        conn.send(b'OK')



#TODO: Сервер может возвращать ошибки
def handle_client(conn, addr):
    """Отдельный поток для каждого клиента"""
    print(f"[+] Подключился {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        print(f"[?] [{addr}] {data}")
        json_data = json.loads(data)
        type = json_data['type']
        # В зависимости от типа запроса, вызываем разные функции
        if type == 'create':
            create_room(conn)
        elif type == 'join':
            room = json_data['room']
            join_room(conn, room)
        #TODO: move, end, close?, start?
    #TODO: Связать отключение клиента с закрытием комнаты
    conn.close()
    print(f"[-] Отключился {addr}")


def start_server(address: str, port: int) -> socket.socket:
    s = socket.socket()
    s.bind((address, port))
    s.listen(5)
    print("[*] Сервер запущен")
    return s


if __name__ == "__main__":
    server = start_server('localhost', 12345)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
