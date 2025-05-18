import tkinter as tk

class ScrollableWindow(tk.Toplevel):
    def __init__(self, master, title):
        super().__init__(master)
        self.title(title)
        self.geometry("500x400")

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class RatingWindow(ScrollableWindow):
    def __init__(self, master, ratings):
        super().__init__(master, "Рейтинг")
        for player, wins in ratings:
            label = tk.Label(self.scrollable_frame, text=f"{player} {wins} побед")
            label.pack(anchor='w', padx=10, pady=2)

class GamesWindow(ScrollableWindow):
    def __init__(self, master, games):
        super().__init__(master, "Игры")
        for idx, w_p, b_p, winner in games:
            if winner == 'Ничья':
                label = tk.Label(self.scrollable_frame, text=f"{idx} {w_p} VS {b_p}. Ничья")
                label.pack(anchor='w', padx=10, pady=2)
            else:
                label = tk.Label(self.scrollable_frame, text=f"{idx} {w_p} VS {b_p}. Победитель: {winner}")
                label.pack(anchor='w', padx=10, pady=2)