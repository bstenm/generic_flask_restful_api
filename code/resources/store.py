import sqlite3
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('feature1',
                        type=str,
                        required=True,
                        help="Can not be left empty"
                        )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM stores WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return {'store': {'name': row[0], 'feature1': row[1]}}

    @classmethod
    def insert(cls, store):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(f">> {store}")
        query = "INSERT INTO stores VALUES(NULL, ?, ?)"
        cursor.execute(query, (store['name'], store['feature1']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, store):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE stores SET feature1=? WHERE name=?"
        cursor.execute(query, (store['feature1'], store['name']))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        store = self.find_by_name(name)
        return store if store else {'message': 'store not found'}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {'message': f'A store with name "{name}" already exists'}, 400

        data = Store.parser.parse_args()
        store = {'name': name, 'feature1': data['feature1']}

        try:
            self.insert(store)
        except:
            return {'message': 'An error occured inserting the store into the database'}, 500

        return store, 201

    def put(self, name):
        data = Store.parser.parse_args()
        store = self.find_by_name(name)
        updated_store = {'name': name, 'feature1': data['feature1']}

        if store is None:
            try:
                self.insert(updated_store)
            except:
                return {'message': 'An error occured inserting the store into the database'}, 500
        else:
            try:
                self.update(updated_store)
            except:
                return {'message': 'An error occured updating the store in the database'}, 500

        return updated_store

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM stores WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Store successfully deleted'}


class StoreList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM stores"
        result = cursor.execute(query)

        stores = []
        for row in result:
            stores.append({'name': row[0], 'feature1': row[1]})

        return stores
