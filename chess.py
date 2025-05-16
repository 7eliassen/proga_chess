import os
import threading
import tkinter as tk
from client.gui.chess_gui import ChessGUI
from modules.game import Game
from client import *
from modules.socketclient import SocketClient



if __name__ == "__main__":
    path_to_figures = os.path.dirname(os.path.abspath(__file__)) + "\\figures"
    gui = ChessGUI(path_to_figures)
    gui.run()
