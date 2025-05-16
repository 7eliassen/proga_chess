import tkinter as tk
from tkinter import messagebox
from random import randint


class NewGameWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Новая игра")
        self.geometry("300x200")
        self.resizable(False, False)
        self.player1_name = None
        self.player2_name = None
        self.result_ready = False

        self.transient(master)
        self.grab_set()
        self.focus_set()

        tk.Label(self, text="Игрок 1:").pack(pady=(10, 0))
        self.entry1 = tk.Entry(self, width=30)
        self.entry1.pack()

        tk.Label(self, text="Игрок 2:").pack(pady=(10, 0))
        self.entry2 = tk.Entry(self, width=30)
        self.entry2.pack()

        self.shuffle_var = tk.BooleanVar()
        self.shuffle_check = tk.Checkbutton(
            self, text="Перемешать", variable=self.shuffle_var,
        )
        self.shuffle_check.pack(pady=5)

        self.start_button = tk.Button(self, text="Начать", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        name1 = self.entry1.get()
        name2 = self.entry2.get()
        if not name1 or not name2:
            messagebox.showwarning("Ошибка", "Введите имена обоих игроков.")
            return
        # Сохраняем результат
        self.player1_name = name1
        self.player2_name = name2
        if self.shuffle_var.get() == 1:
            self.shuffle_players()
        self.result_ready = True
        self.destroy()  # Закрыть окно

    def shuffle_players(self):
        is_shuffle = randint(0, 1)
        if is_shuffle:
            self.player1_name, self.player2_name = self.player2_name, self.player1_name
