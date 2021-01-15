from database import DB

class Friend:
    def __init__(self, friend_id, name):
        self.friend_id = friend_id
        self.name = name

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
