from modules.errors import InvalidMoveError


def check_bounds(move_func):
    def wrapper(self, new_pos_x, new_pos_y):
        if not (1 <= new_pos_x <= 8 and 1 <= new_pos_y <= 8):
            raise InvalidMoveError("Figure beyond the borders")
        return move_func(self, new_pos_x, new_pos_y)
    return wrapper