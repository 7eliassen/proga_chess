import os
from gui.chess_gui import ChessGUI
from modules.game import Game



if __name__ == "__main__":
    path_to_figures = os.path.dirname(os.path.abspath(__file__)) + "\\figures"
    game = Game()
    gui = ChessGUI(path_to_figures)
    gui.run()
