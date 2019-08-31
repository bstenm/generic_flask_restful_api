import sqlite3
from flask_restful import Resource, reqparse


class User:
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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="A username should be provided"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="A password should be provided"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        password = data['password']
        username = data['username']

        if User.find_by_username(username):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        # TODO: encrypt password
        cursor.execute(query, (username, password))

        connection.commit()
        connection.close()

        return {'message': 'User successfully created'}, 201
