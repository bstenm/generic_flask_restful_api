import sqlite3


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.password = password
        self.username = username

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # execute query passing a tuple
        query = "SELECT * from users where username=?"
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        connection.close()

        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        # execute query passing a tuple
        query = "SELECT * from users where id=?"
        cursor.execute(query, (_id,))
        row = cursor.fetchone()
        connection.close()

        return cls(*row) if row else None
