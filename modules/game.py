from modules.errors import EmptyFieldError, OutOfBoundsError, SetIdError
from modules.figures import *


class Game:
    def __init__(self):
        self.__board = self.create_board()
        self.__status = 'wait'
        self.id = None
        self.player1 = None
        self.player2 = None
        self.turn = 'white'

    def __str__(self):
        return f'Game({self.id}) is {self.get_status()} P1:{self.player1} | P2:{self.player2}'

    def get_current_player(self):
        if self.turn == 'white':
            return self.player1
        elif self.turn == 'black':
            return self.player2

    def get_opponent_player(self):
        if self.turn == 'white':
            return self.player2
        elif self.turn == 'black':
            return self.player1

    def set_player(self, number, user):
        if number == 1:
            self.player1 = user
        elif number == 2:
            self.player2 = user


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
        board = "\n"
        board += "   0 1 2 3 4 5 6 7\n"
        board += "  ________________\n"
        for row in range(8):
            line = f"{row} |"
            for col in range(8):
                piece = self.__board[row][col]
                if piece:
                    line += f"{str(piece)}|"
                else:
                    line += " |"
            board += line + "\n"
        board += "  ----------------\n"
        board += "   0 1 2 3 4 5 6 7\n"

        return board

    def make_move(self, pos_x, pos_y, new_pos_x, new_pos_y, team='test'):
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        new_pos_y = int(new_pos_y)
        new_pos_x = int(new_pos_x)
        board = self.__board
        piece = board[pos_y][pos_x]
        if piece:
            move_ = piece.move(new_pos_x, new_pos_y)
            if move_:
                board[new_pos_y][new_pos_x] = piece
                board[pos_y][pos_x] = None
                if self.turn == 'white':
                    self.turn = 'black'
                elif self.turn == 'black':
                    self.turn = 'white'
                return move_
            else:
                raise InvalidMoveError
        else:
            raise EmptyFieldError
