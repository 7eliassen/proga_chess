'''Тут будет находиться клиентская часть приложения'''
import socket
import json


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
    print(json_data['room_id'])



def connect_to_room(client, room, name='TEST_NAME'):
    """Подключение к комнате. Отправка данных в JSON"""
    data = {'type': 'join',
            'name': name,
            'room': room}
    json_str = json.dumps(data)
    message = json_str.encode()
    client.send(message)


if __name__ == '__main__':
    client = connection_to_server('localhost', 12345)
    create_room(client)
    client.close()
