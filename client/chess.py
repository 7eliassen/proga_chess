import os
import threading
import tkinter as tk
from gui.chess_gui import ChessGUI
from modules.errors import EmptyFieldError
from modules.game import Game


def simple_console_interface(game:Game, gui):
    print("Шахматная игра (консольный режим)")
    print(game.print_board())

    while True:
        print(f"Ходит: {game.turn}")
        move = input("Введите ход (формат: x_from y_from x_to y_to) или 'exit': ")
        if move.lower() == 'exit':
            print("Игра завершена.")
            break

        try:
            x1, y1, x2, y2 = move.split()
            game.make_move(x1, y1, x2, y2)
            print(game.print_board())
            gui.root.after(0, gui.update_board)
        except ValueError:
            print("Ошибка: введите 4 числа через пробел.")
        except EmptyFieldError:
            print("Ошибка: выбранная клетка пуста.")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    path_to_figures = os.path.dirname(os.path.abspath(__file__)) + "\\figures"
    game = Game()
    gui = ChessGUI(path_to_figures, game)
    threading.Thread(target=simple_console_interface, args=(game,gui), daemon=True).start()
    gui.run()