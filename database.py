import sqlite3

DB_NAME = 'chat_application.db'

conn = sqlite3.connect(DB_NAME)


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS friends
    (
        friend_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT
    )
''')
conn.commit()


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS Messages
    (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        sent_by  TEXT,
        content TEXT,
        FOREIGN KEY(receiver_id) REFERENCES friends(friend_id)
    )
''')
conn.commit()



class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
