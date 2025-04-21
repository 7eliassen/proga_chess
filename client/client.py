'''Тут будет находиться клиентская часть приложения'''
import socket
import json
import logging
import signal
import sys

socket_ = None

logging.basicConfig(
    level=logging.DEBUG,  # INFO или DEBUG для подробностей
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename=None,  # можно None — тогда в консоль
    filemode='w'  # 'a' — добавлять, 'w' — перезаписывать
)

def close_socket_and_exit(signum, frame):
    """Обработчик сигнала для закрытия сокета перед выходом."""
    global client_socket
    if client_socket:
        print("\nЗакрытие сокета и выход...")
        socket_.close()  # Закрываем сокет
    sys.exit(0)
signal.signal(signal.SIGINT, close_socket_and_exit)

def connection_to_server(address: str, port: int) -> socket.socket:
    s = socket.socket()
    s.connect((address, port))
    return s


def init_game():
    """После создания/подключения к комнате инициализируется игра"""


def create_room(client, name='TEST_NAME') -> int:
    """Создание комнаты. Сервер возвращает номер комнаты"""
    data = {'type': 'create',
            'name': name}
    json_str = json.dumps(data)
    message = json_str.encode()
    client.send(message)

    r_message = client.recv(1024).decode()
    json_data = json.loads(r_message)
    logging.debug(json_data)
    logging.info("Ожидаем оппонента")

    r_message = client.recv(1024).decode()
    json_data = json.loads(r_message)
    logging.debug(json_data)
    if json_data['type'] == 'join':
        if json_data['code'] == 'opponent_is_found':
            return json_data['room_id']
        else:
            return 0


def connect_to_room(client, room, name='TEST_NAME'):
    """Подключение к комнате. Отправка данных в JSON"""
    data = {'type': 'join',
            'name': name,
            'room': room}
    json_str = json.dumps(data)
    message = json_str.encode()
    client.send(message)
    r_message = client.recv(1024).decode()
    json_data = json.loads(r_message)
    logging.debug(json_data)
    if json_data['type'] == 'join':
        if json_data['code'] == 'successful':
            return json_data['room_id']
        else:
            return 0


if __name__ == '__main__':
    client = connection_to_server('localhost', 12345)
    create_room(client)
    client.close()
