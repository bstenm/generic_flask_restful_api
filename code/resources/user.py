import sqlite3
from models.user import UserModel
from flask_restful import Resource, reqparse


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

        if UserModel.find_by_username(username):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL, ?, ?)"
        # TODO: encrypt password
        cursor.execute(query, (username, password))

        connection.commit()
        connection.close()

        return {'message': 'User successfully created'}, 201
