from modules.errors import EmptyFieldError, OutOfBoundsError, SetIdError
from modules.figures import *


class Game:
    def __init__(self):
        self.__board = self.create_board()
        self.__status = 'wait'
        self.__id = None
        self.player1 = None
        self.player2 = None

    def __str__(self):
        return f'Game({self.__id}) is {self.get_status()}'

    def set_player(self, number, user):
        if number == 1:
            self.player1 = user
        elif number == 2:
            self.player2 = user

    def get_id(self):
        return self.__id

    def set_id(self, id):
        if 1000 <= id <= 9999:
            self.__id = id
        else: raise SetIdError

    def get_status(self):
        return self.__status

    def set_status(self, status):
        if status in ['wait', 'both_connected', 'in_process', 'finished']:
            self.__status = status

    def create_board(self):
        # Создаем пустую доску 8x8
        board = [[None] * 8 for _ in range(8)]

        # Размещаем черные фигуры (индексация в массиве начинается с 0)
        board[0][0] = Rook(0, 0, 'black')
        board[0][1] = Knight(1, 0, 'black')
        board[0][2] = Bishop(2, 0, 'black')
        board[0][3] = Queen(3, 0, 'black')
        board[0][4] = King(4, 0, 'black')
        board[0][5] = Bishop(5, 0, 'black')
        board[0][6] = Knight(6, 0, 'black')
        board[0][7] = Rook(7, 0, 'black')

        # Размещаем черные пешки
        for col in range(8):
            board[1][col] = Pawn(col, 1, 'black')

        # Размещаем белые пешки
        for col in range(8):
            board[6][col] = Pawn(col, 6, 'white')

        # Размещаем белые фигуры
        board[7][0] = Rook(0, 7, 'white')
        board[7][1] = Knight(1, 7, 'white')
        board[7][2] = Bishop(2, 7, 'white')
        board[7][3] = Queen(3, 7, 'white')
        board[7][4] = King(4, 7, 'white')
        board[7][5] = Bishop(5, 7, 'white')
        board[7][6] = Knight(6, 7, 'white')
        board[7][7] = Rook(7, 7, 'white')

        return board

    def print_board(self):
        """
        Отображает текущее состояние доски.
        """
        print("   0 1 2 3 4 5 6 7")
        print("  ________________")
        for row in range(8):
            line = f"{row} |"
            for col in range(8):
                piece = self.__board[row][col]
                if piece:
                    line += f"{str(piece)}|"
                else:
                    line += " |"
            print(line)
        print("  ----------------")
        print("   0 1 2 3 4 5 6 7")

    def make_move(self, pos_x, pos_y, new_pos_x, new_pos_y, team='test'):
        board = self.__board
        piece = board[pos_y][pos_x]
        if piece:
            if piece.move(new_pos_x, new_pos_y):
                board[new_pos_y][new_pos_x] = piece
                board[pos_y][pos_x] = None
            else:
                raise InvalidMoveError
        else:
            raise EmptyFieldError
