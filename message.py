from database import DB

class Message:
    def __init__(self, message_id, author, content):
        self.message_id = message_id
        self.author = author
        self.content = content

    @staticmethod
    def all():
        with DB as db:
            rows = db.execute('SLECT * FROM messages').fetchall()
            return [Message(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.author, self.content)
            row = db.execute('INSERT INTO messages (author, content) VALUES (?, ?)', values)
            return self
