import os
from gui.chess_gui import ChessGUI

if __name__ == "__main__":
    path_to_figures = os.path.dirname(os.path.abspath(__file__)) + "\\figures"
    gui = ChessGUI(path_to_figures)
    gui.run()
