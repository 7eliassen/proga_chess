from modules.game import *
game = Game()
game.print_board()
#Пешка ходит вперед
game.make_move(4, 6, 4, 5)
game.print_board()
game.make_move(3, 1, 3, 2)
game.print_board()
#Ходит конь
game.make_move(6, 7, 7, 5)
game.print_board()
game.make_move(1, 0, 2, 2)
game.print_board()
#Ферзь
game.make_move(3, 7, 4, 6)
game.print_board()
game.make_move(3, 0, 3, 1)
game.print_board()
#Еще ферзь
game.make_move(4, 6, 7, 3)
game.print_board()

try:
    # Пример неверного хода (пешка пытается перепрыгнуть через клетку)
    game.make_move(0, 1, 0, 4)
except InvalidMoveError: print("Неверный ход")

try:
    game.make_move(0, 1, 0, 9)
except InvalidMoveError: print("Вышел за граница")
