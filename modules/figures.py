"""В этом файле содержатся классы шахматных фигур"""
from modules.errors import InvalidMoveError
from modules.logic import check_bounds

"""
Pawn – Пешка
Knight – Конь
Bishop – Слон
Rook – Ладья
Queen – Ферзь
King – Король
"""


class Figure:
    def __init__(self, pos_x, pos_y, team):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__team = team  # 'white' или 'black'

    def __str__(self):
        return "T"


    def get_team(self):
        return self.__team

    def move(self, pos_x, pos_y):
        self.__pos_y = pos_y
        self.__pos_x = pos_x
        return True

    def get_position(self):
        return [self.__pos_x, self.__pos_y]


class Pawn(Figure):
    # TODO: Пешка может есть по диагонали
    # TODO: Пешка может превратиться в другую фигуру (класс/цикл)?

    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "P"

    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        team = self.get_team()
        pos_x, pos_y = self.get_position()
        if team == 'black' and \
                pos_x == new_pos_x and pos_y + 1 == new_pos_y:
            return super().move(new_pos_x, new_pos_y)
        elif team == 'white' and \
                pos_x == new_pos_x and pos_y - 1 == new_pos_y:
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError('Invalid move for Pawn')


class Knight(Figure):
    # TODO: шах и мат

    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "Л"

    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        pos_x, pos_y = self.get_position()
        # Проверка на "букву Г"
        if (abs(new_pos_x - pos_x) == 2 and abs(new_pos_y - pos_y) == 1) or \
                (abs(new_pos_x - pos_x) == 1 and abs(new_pos_y - pos_y) == 2):
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError("Invalid move for Knight.")


class Bishop(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "B"


    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        pos_x, pos_y = self.get_position()
        # Слон двигается по диагоналям, то есть разница по обеим осям должна быть одинаковой
        if abs(new_pos_x - pos_x) == abs(new_pos_y - pos_y):
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError("Invalid move for Bishop.")


class Rook(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "R"

    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        pos_x, pos_y = self.get_position()
        # Ладья двигается по прямым линиям: либо по вертикали, либо по горизонтали
        if pos_x == new_pos_x or pos_y == new_pos_y:
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError("Invalid move for Rook.")


class Queen(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "Q"

    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        pos_x, pos_y = self.get_position()
        # Ферзь может двигаться как слон и как ладья
        if abs(new_pos_x - pos_x) == abs(new_pos_y - pos_y) or \
                pos_x == new_pos_x or pos_y == new_pos_y:
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError("Invalid move for Queen.")


class King(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "K"

    @check_bounds
    def move(self, new_pos_x, new_pos_y):
        pos_x, pos_y = self.get_position()
        # Король может двигаться на одно поле в любом направлении
        if abs(new_pos_x - pos_x) <= 1 and abs(new_pos_y - pos_y) <= 1:
            return super().move(new_pos_x, new_pos_y)
        else:
            raise InvalidMoveError("Invalid move for King.")
