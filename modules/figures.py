"""В этом файле содержатся классы шахматных фигур"""
from modules.errors import InvalidMoveError, OutOfBoundsError

"""
Pawn – Пешка
Knight – Конь
Bishop – Слон
Rook – Ладья
Queen – Ферзь
King – Король
"""


# Класс-миксин для логирования
class LoggerMixin:
    def log_move(self, from_pos, to_pos, team):
        print(f"[LOG] {self.__class__.__name__} from {team} moved from {from_pos} to {to_pos}")


# Родительский класс фигуры
class Figure(LoggerMixin):
    def __init__(self, pos_x, pos_y, team):
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__team = team

    def __str__(self):
        return "T"

    def can_attack(self, x, y, board):
        pass

    def get_team(self):
        return self.__team

    def debug_move(self, pos_x, pos_y):
        self.move(pos_x, pos_y)

    def move(self, pos_x, pos_y, piece_2=None):
        if not (0 <= pos_x <= 7 and 0 <= pos_y <= 7):
            raise OutOfBoundsError("Figure beyond the borders")

        old_x, old_y = self.get_position()
        self.__pos_y = pos_y
        self.__pos_x = pos_x
        self.log_move(f"X:{old_x} Y:{old_y}", f"X:{pos_x} Y:{pos_y} and eat {piece_2}", self.get_team())
        return True

    def get_position(self):
        return [self.__pos_x, self.__pos_y]

    # Метод для отладки, никаких проверок
    def set_position(self, pos_x, pos_y):
        old_x, old_y = self.get_position()
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.log_move(f"X:{old_x} Y:{old_y}", f"X:{pos_x} Y:{pos_y}", self.get_team())


class Pawn(Figure):

    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "P"

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()
        direction = 1 if self.get_team() == 'black' else -1
        return (abs(x - pos_x) == 1) and (y - pos_y == direction)

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        team = self.get_team()
        pos_x, pos_y = self.get_position()
        dx = new_pos_x - pos_x
        dy = new_pos_y - pos_y
        if team == 'black':
            if dx == 0 and dy == 1 and not piece_2:
                return super().move(new_pos_x, new_pos_y)
            elif dx == 0 and dy == 2 and not piece_2 and pos_y == 1:
                return super().move(new_pos_x, new_pos_y)
            elif piece_2 and dy == 1 and abs(dx) == 1 \
                    and piece_2.get_team() != team:
                return super().move(new_pos_x, new_pos_y, piece_2)
        elif team == 'white':
            if dx == 0 and dy == -1 and not piece_2:
                return super().move(new_pos_x, new_pos_y, piece_2)
            elif dx == 0 and dy == -2 and not piece_2 and pos_y == 6:
                return super().move(new_pos_x, new_pos_y)
            elif piece_2 and dy == -1 and abs(dx) == 1 \
                    and piece_2.get_team() != team:
                return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError('Invalid move for Pawn')


class Knight(Figure):

    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "H"

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()
        dx = abs(x - pos_x)
        dy = abs(y - pos_y)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        pos_x, pos_y = self.get_position()
        # Проверка на "букву Г"
        if (abs(new_pos_x - pos_x) == 2 and abs(new_pos_y - pos_y) == 1) or \
                (abs(new_pos_x - pos_x) == 1 and abs(new_pos_y - pos_y) == 2):
            return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError("Invalid move for Knight.")


class Bishop(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "B"

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()
        if abs(x - pos_x) != abs(y - pos_y):
            return False
        return True

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        pos_x, pos_y = self.get_position()
        # Слон двигается по диагоналям, то есть разница по обеим осям должна быть одинаковой
        dy = abs(new_pos_y - pos_y)
        dx = abs(new_pos_x - pos_x)
        if dy == dx:
            return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError("Invalid move for Bishop.")


class Rook(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "R"

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()
        if pos_x != x and pos_y != y:
            return False
        return True

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        pos_x, pos_y = self.get_position()
        # Ладья двигается по прямым линиям: либо по вертикали, либо по горизонтали
        if pos_x == new_pos_x or pos_y == new_pos_y:
            return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError("Invalid move for Rook.")


class Queen(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def __str__(self):
        return "Q"

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()

        def bishop():
            if abs(x - pos_x) != abs(y - pos_y):
                return False
            return True

        def rook():
            if pos_x != x and pos_y != y:
                return False
            return True

        return bishop() or rook()

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        pos_x, pos_y = self.get_position()
        # Ферзь может двигаться как слон и как ладья
        if abs(new_pos_x - pos_x) == abs(new_pos_y - pos_y) or \
                pos_x == new_pos_x or pos_y == new_pos_y:
            return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError("Invalid move for Queen.")


class King(Figure):
    def __init__(self, pos_x, pos_y, team):
        super().__init__(pos_x, pos_y, team)

    def is_can_attack(self, x, y):
        pos_x, pos_y = self.get_position()
        return abs(x - pos_x) <= 1 and abs(y - pos_y) <= 1

    def __str__(self):
        return "K"

    def move(self, new_pos_x, new_pos_y, piece_2=None):
        pos_x, pos_y = self.get_position()
        # Король может двигаться на одно поле в любом направлении
        if abs(new_pos_x - pos_x) <= 1 and abs(new_pos_y - pos_y) <= 1:
            return super().move(new_pos_x, new_pos_y, piece_2)
        else:
            raise InvalidMoveError("Invalid move for King.")
