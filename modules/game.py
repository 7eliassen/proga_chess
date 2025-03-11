from modules.figures import *
class Game:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = [[None] * 8 for _ in range(8)]  # 8x8 доска

        # Размещение фигур на доске
        board[0] = [
            Rook(1, 1, 'black'), Knight(2, 1, 'black'), Bishop(3, 1, 'black'), Queen(4, 1, 'black'),
            King(5, 1, 'black'), Bishop(6, 1, 'black'), Knight(7, 1, 'black'), Rook(8, 1, 'black')
        ]
        board[1] = [Pawn(x + 1, 2, 'black') for x in range(8)]  # Черные пешки
        board[6] = [Pawn(x + 1, 7, 'white') for x in range(8)]  # Белые пешки
        board[7] = [
            Rook(1, 8, 'white'), Knight(2, 8, 'white'), Bishop(3, 8, 'white'), Queen(4, 8, 'white'),
            King(5, 8, 'white'), Bishop(6, 8, 'white'), Knight(7, 8, 'white'), Rook(8, 8, 'white')
        ]
        return board

    def print_board(self):
        for row in range(8):
            line = f"{row}|"
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    line += f"{str(piece)}|"
                else:
                    line += " |"
            print(line)
            print("-" * 18)
        print(" |0|1|2|3|4|5|6|7|")

