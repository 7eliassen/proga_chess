class InvalidMoveError(Exception):
    """Ошибка: недопустимый ход в шахматах"""
    def __init__(self, message="Недопустимый ход"):
        self.message = message
        super().__init__(self.message)

class EmptyFieldError(Exception):
    """Пустое поле"""
    def __init__(self, message="Пустое поле"):
        self.message = message
        super().__init__(self.message)
