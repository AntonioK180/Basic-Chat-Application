from database import DB

class Friend:
    def __init__(self, friend_id, name, nickname):
        self.friend_id = friend_id
        self.name = name
        self.nickname = nickname


    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM friends').fetchall()
            return [Friend(*row) for row in rows]

    @staticmethod
    def find(friend_id):
        with DB() as db:
            row = db.execute('SELECT * FROM friends WHERE friend_id = ?', (friend_id,)).fetchone()
            if row is None:
                return
            return Friend(*row)

    @staticmethod
    def find_by_name(name):
        with DB() as db:
            row = db.execute('SELECT * FROM friends WHERE name = ?', (name,)).fetchone()
            if row is None:
                return
            return Friend(*row)

    def create(self):
        with DB() as db:
            row = db.execute('INSERT INTO friends (name, nickname) VALUES (?, ?)', (self.name, self.nickname))
            return self

    def save(self):
        with DB() as db:
            values = (self.nickname, self.name)
            db.execute('UPDATE friends SET nickname = ? WHERE name = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM Messages WHERE receiver_id = ?', (self.friend_id,))
            db.execute('DELETE FROM friends WHERE friend_id = ?', (self.friend_id,))
