"""Тут будет нахоиться серверная часть приложения"""
# TODO: добавить логирование
# TODO: добавить везде обработки ошибок
import socket
import threading
import json
import random
import modules.game as game
import logging
import uuid
from modules.user import User

logging.basicConfig(
    level=logging.DEBUG,  # INFO или DEBUG для подробностей
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename=None,  # можно None — тогда в консоль
    filemode='w'  # 'a' — добавлять, 'w' — перезаписывать
)

# uuid: socket-connection
users = {}

#FIXME: временно
# room_id(int): [game, who_wait]
games = {}


def create_room(user:User):
    """Здесь будет создание комнаты"""
    conn = user.conn
    new_game = game.Game()
    #TODO: модифицировать проверку на коллизии
    room_id = random.randint(1000, 9999)
    while room_id in games.keys():
        room_id = random.randint(1000, 9999)
    new_game.set_id(room_id)
    games[room_id] = [new_game, conn]
    new_game.set_player(1, user)
    logging.info(f'Пользователь {user} создал комнату [{new_game}]')
    logging.debug(f"Список комнат: {games}")
    data = {'type': 's_room_id',
            'room_id': room_id}
    json_data = json.dumps(data)
    message = json_data.encode()
    conn.send(message)

def join_room(user:User, room_id:str):
    #FIXME: Создать настоящее присоединение к комнате
    conn = user.conn
    logging.debug(f"Пользователь {user} пытается подключиться к {room_id}")
    aviable_games =list(games.keys())
    logging.debug(f"Список текущих игр: {aviable_games}")
    room_id = int(room_id)
    if room_id in aviable_games:
        game, conn2 = games[room_id]
        #FIXME: Отправка данных по JSON
        conn2.send(b"opponent is found")
        conn.send(b'OK')
        game.set_status('both_connected')
        logging.info(f'Пользователь {user} подключился к [{game}]')
    else:
        logging.debug(f"Пользователь {user} не смог подключиться к {room_id}")


#TODO: Сервер может возвращать ошибки
def handle_client(user_id:str):
    """Отдельный поток для каждого клиента"""
    user = users[user_id]
    conn = user.conn
    addr = user.addr
    logging.info(f"Подключился {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        logging.debug(f"[{addr}] {data}")
        json_data = json.loads(data)
        type = json_data['type']
        # В зависимости от типа запроса, вызываем разные функции
        if type == 'create':
            create_room(user)
        elif type == 'join':
            room = json_data['room']
            join_room(user, room)
        #TODO: move, end, close?, start?
    #TODO: Связать отключение клиента с закрытием комнаты
    conn.close()
    logging.info(f"Отключился {addr}")


def start_server(address: str, port: int) -> socket.socket:
    s = socket.socket()
    s.bind((address, port))
    s.listen(5)
    logging.info("Сервер запущен")
    return s


if __name__ == "__main__":
    server = start_server('localhost', 12345)
    while True:
        conn, addr = server.accept()
        user_id = str(uuid.uuid4())
        users[user_id] = User(user_id=user_id, conn=conn, addr=addr)
        logging.debug(f'USERS: {users[user_id]}')
        thread = threading.Thread(target=handle_client, args=[user_id])
        thread.start()
