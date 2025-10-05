import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from modules.game import Game
from .new_game_pop import NewGameWindow
from .statistics import *
from modules.database import *

IS_DEBUG = 0


class ChessGUI():
    def __init__(self, figures_path):
        self.root = tk.Tk()
        self.game = None
        self.root.title("Шахматы")
        self.cell_size = 80
        self.canvas = tk.Canvas(self.root, width=8 * self.cell_size, height=8 * self.cell_size)
        self.canvas.pack()
        self.win_height = self.cell_size * 8 + 100
        self.win_width = self.cell_size * 8
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.figures_path = figures_path
        self.pieces = {}

        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Начать", command=self.new_game)
        menubar.add_cascade(label="Игра", menu=game_menu)

        statistic = tk.Menu(menubar, tearoff=0)
        statistic.add_command(label="Рейтинг", command=self.view_rating)
        statistic.add_command(label="Игры", command=self.view_games)

        menubar.add_cascade(label="Статистика", menu=statistic)

        self.root.config(menu=menubar)

        self.label_turn = tk.Label(self.root, text="", font=("Arial", 16))
        self.label_turn.pack(pady=10)

        self.draw_button = tk.Button(self.root, font=("Arial", 16), text="Ничья", command=self.declare_draw)

        self.selected_cell = None
        if IS_DEBUG:
            self.start_game()

    def declare_draw(self):
        add_game(self.game.player1, self.game.player2, "Ничья")
        messagebox.showinfo('Ничья', "Объявлена ничья")
        self.end_game()

    def view_games(self):
        games = get_all_games()
        GamesWindow(self.root, games)

    def view_rating(self):
        ratings = get_rating()
        RatingWindow(self.root, ratings)

    def new_game(self):
        new_game_win = NewGameWindow(self.root)
        self.root.wait_window(new_game_win)
        if new_game_win.result_ready:
            player1 = new_game_win.player1_name[0:10]
            player2 = new_game_win.player2_name[0:10]
            messagebox.showinfo("Игроки выбраны", f"Игрок 1: {player1}\nИгрок 2: {player2}")
        else:
            messagebox.showinfo("Отмена", "Игра не была начата")
            return
        self.start_game(player1, player2)

    def start_game(self, player1="TEST1", player2="TEST2"):
        new_game = Game()
        new_game.set_player(1, player1)
        new_game.set_player(2, player2)

        self.game = new_game

        self.canvas.bind("<Button-1>", self.on_click)
        self.update_board()
        self.draw_button.pack(pady=10)

    def run(self):
        self.root.mainloop()

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_cell is None:
            self.selected_cell = (col, row)
            self.update_board()
        else:
            from_x, from_y = self.selected_cell
            to_x, to_y = col, row

            try:
                result = self.game.make_move(from_x, from_y, to_x, to_y, debug_mode=IS_DEBUG)
                if result == 'check':
                    messagebox.showinfo("ШАХ", "ШАХ")
                elif result == 'checkmate':
                    team, nick_mane = ('Белые', self.game.player1) if self.game.turn == 'black' else (
                        'Черные', self.game.player2)
                    messagebox.showinfo('МАТ', f'Цвет: {team}\n{nick_mane} победил')
                    add_game(self.game.player1, self.game.player2, nick_mane)
                    self.end_game()
                    return
                elif result == 'check_move':
                    messagebox.showinfo('ШАХ', 'Вам нужно избавиться от шаха')



            except Exception as error:
                messagebox.showerror("Ошибка", str(error))

            self.selected_cell = None
            self.update_board()

    def end_game(self):
        self.game = None
        self.canvas.delete("all")
        self.label_turn.config(text="")
        self.selected_cell = None
        self.draw_button.pack_forget()

    def draw_board(self):
        colors = ["#EEEED2", "#769656"]
        highlight_color = "#FF6666"
        for row in range(8):
            for col in range(8):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.selected_cell == (col, row):
                    color = highlight_color
                else:
                    color = colors[(row + col) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        if self.game.turn == 'white':
            self.label_turn.config(text=f"Сейчас ходят белые")
        elif self.game.turn == 'black':
            self.label_turn.config(text=f"Сейчас ходят черные")

    def load_piece(self, name):
        if name in self.pieces:
            return self.pieces[name]
        path = os.path.join(self.figures_path, f"{name}.png")
        image = Image.open(path)
        image = image.resize((self.cell_size, self.cell_size))
        tk_image = ImageTk.PhotoImage(image)
        self.pieces[name] = tk_image
        return tk_image

    def draw_pieces(self):
        board_state = self.game.get_board()
        for row in range(8):
            for col in range(8):
                piece = board_state[row][col]
                if piece:
                    name_piece = ""
                    if piece.get_team() == 'white':
                        name_piece += "w_"
                    else:
                        name_piece += "b_"
                    name_piece += str(piece)
                    img = self.load_piece(name_piece)
                    x = col * self.cell_size
                    y = row * self.cell_size
                    self.canvas.create_image(x, y, anchor='nw', image=img)

    def update_board(self):
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
