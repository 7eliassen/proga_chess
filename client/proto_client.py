import logging

from client import *

def init_game(client: socket.socket):
    print("Инициализация игры...")

    # Получаем стартовое сообщение от сервера (цвет игрока и id комнаты)

    r_message = client.recv(1024).decode()
    logging.debug(r_message)
    info = json.loads(r_message)
    color = info.get('your_color')
    room_id = info.get('room_id')
    logging.info(f"Вы играете за: {color}")
    logging.debug(info)

    while True:
        message = client.recv(1024).decode()
        data = json.loads(message)
        logging.debug(data)

        if data['type'] == 'your_turn':
            print("Ваш ход.")
            from_cell = input("Откуда (например, 1 1): ")
            to_cell = input("Куда (например 1 2): ")
            move = {
                'type': 'move',
                'room_id': room_id,
                'from': from_cell,
                'to': to_cell
            }
            client.send(json.dumps(move).encode())

        elif data['type'] == 'opponent_move':
            print(f"Ход соперника: {data['from']} -> {data['to']}")

            print("Ваш ход.")
            from_cell = input("Откуда (например, 1 1): ")
            to_cell = input("Куда (например 1 2): ")
            move = {
                'type': 'move',
                'room_id': room_id,
                'from': from_cell,
                'to': to_cell
            }

            client.send(json.dumps(move).encode())


        elif data['type'] == 'game_over':
            print("Игра окончена.")
            break

        else:
            print(f"Неизвестный тип сообщения: {data}")

def main_menu():
    print("=== Добро пожаловать в шахматы ===")
    print("1. Создать комнату")
    print("2. Подключиться к комнате")
    print("0. Выход")

def debug_interface():
    client = connection_to_server('localhost', 12345)
    while True:
        main_menu()
        choice = input("Выберите действие: ")

        if choice == '1':
            room_id = create_room(client)
            if room_id != 0:
                init_game(client)

        elif choice == '2':
            room_id = input("Введите ID комнаты: ")
            room_id = connect_to_room(client, room_id)
            if room_id != 0:
                init_game(client)

        elif choice == '0':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

    client.close()

# Запуск интерфейса
if __name__ == '__main__':
    debug_interface()