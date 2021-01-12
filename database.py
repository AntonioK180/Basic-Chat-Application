import sqlite3

DB_NAME = 'chat.db'

conn = sqlite3.connect(DB_NAME)


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS messages
    (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT,
        content TEXT
    )
''')

conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
