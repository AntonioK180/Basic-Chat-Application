from database import DB

class Message:
    def __init__(self, message_id, sender_id, receiver_id, sent_by, content):
        self.message_id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.sent_by = sent_by
        self.content = content

    @staticmethod
    def all_with(friend_id):
        with DB() as db:
            rows = db.execute('SELECT * FROM Messages WHERE receiver_id = ?', (friend_id,)).fetchall()
            return [Message(*row) for row in rows]

    def create(self):
        with DB() as db:
            values = (self.sender_id, self.receiver_id, self.sent_by, self.content)
            row = db.execute('INSERT INTO Messages(sender_id, receiver_id, sent_by, content) VALUES (?, ?, ?, ?)', values)
            return self
