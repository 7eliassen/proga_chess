from modules.errors import InvalidMoveError, OutOfBoundsError


def check_bounds(move_func):
    def wrapper(self, new_pos_x, new_pos_y):
        if not (0 <= new_pos_x <= 7 and 0 <= new_pos_y <= 7):
            raise OutOfBoundsError("Figure beyond the borders")
        return move_func(self, new_pos_x, new_pos_y)
    return wrapper
