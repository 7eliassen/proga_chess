class InvalidMoveError(Exception):
    """Ошибка: недопустимый ход в шахматах"""
    def __init__(self, message="Недопустимый ход"):
        self.message = message
        super().__init__(self.message)
