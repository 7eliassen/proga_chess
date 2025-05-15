import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
import os

IS_DEBUG = False


class ChessGUI:
    def __init__(self, figures_path, game):
        self.root = tk.Tk()
        self.game = game
        self.root.title("Шахматы с фигурами")
        self.cell_size = 80
        self.canvas = tk.Canvas(self.root, width=8 * self.cell_size, height=8 * self.cell_size)
        self.canvas.pack()
        self.win_height = self.cell_size * 8 + 100
        self.win_width = self.cell_size * 8
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.figures_path = figures_path
        self.pieces = {}  # Сюда загрузим изображения
        self.canvas.bind("<Button-1>", self.on_click)

        self.label_turn = tk.Label(self.root, text="", font=("Arial", 16))
        self.label_turn.pack(pady=20)
        self.selected_cell = None
        self.update_board()

    def run(self):
        self.root.mainloop()

    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected_cell is None:
            # Первая клетка выбрана
            self.selected_cell = (col, row)
            self.update_board()
        else:
            # Вторая клетка — делаем ход
            from_x, from_y = self.selected_cell
            to_x, to_y = col, row

            try:
                self.game.make_move(from_x, from_y, to_x, to_y, debug_mode=IS_DEBUG)
            except Exception as error:
                messagebox.showerror("Ошибка", str(error))

            self.selected_cell = None
            self.update_board()

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
