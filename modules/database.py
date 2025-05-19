import sqlite3


def create_database():
    conn = sqlite3.connect('chess_games.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        white_player TEXT,
        black_player TEXT,
        who_win TEXT
    )
    ''')
    conn.commit()
    conn.close()


def add_game(white_player, black_player, winner):
    conn = sqlite3.connect('chess_games.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO games (date, white_player, black_player, who_win)
    VALUES (datetime('now'), ?, ?, ?);
    ''', (white_player, black_player, winner))
    conn.commit()
    conn.close()


def get_all_games():
    conn = sqlite3.connect('chess_games.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID,white_player,black_player,who_win FROM games ORDER BY ID DESC')
    rows = cursor.fetchall()
    conn.close()

    return rows


def get_rating():
    conn = sqlite3.connect('chess_games.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT who_win, COUNT(*) as win_count
    FROM games
    WHERE who_win != "Ничья"
    GROUP BY who_win
    ORDER BY win_count DESC;
    ''')
    rows = cursor.fetchall()
    conn.close()

    return rows
