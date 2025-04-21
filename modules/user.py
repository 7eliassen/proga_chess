class User:
    def __init__(self, user_id, conn, addr):
        self.user_id = user_id
        self.conn = conn
        self.addr = addr

    def __str__(self):
        return f"{self.user_id[:5]}"