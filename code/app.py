from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister
import credentials

app = Flask(__name__)
app.secret_key = credentials.jwt_key
api = Api(app)

# create a new endpoint '/auth'
jwt = JWT(app, authenticate, identity)

stores = []


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('feature1',
                        type=str,
                        required=True,
                        help="Can not be left empty"
                        )

    @jwt_required()
    def get(self, name):
        matches = filter(lambda store: store['name'] == name, stores)
        store = next(matches, None)
        return {'store': store}

    def post(self, name):
        data = Store.parser.parse_args()
        matches = filter(lambda store: store['name'] == name, stores)
        if next(matches, None):
            return {'message': f'A store with name "{name}" already exists'}, 400

        store = {'name': name, 'feature1': data['feature1']}
        stores.append(store)
        return store, 201

    def put(self, name):
        data = Store.parser.parse_args()
        matches = filter(lambda store: store['name'] == name, stores)
        store = next(matches, None)
        if store is None:
            store = {'name': name, 'feature1': data['feature1']}
            stores.append(store)
        else:
            store.update(data)
        return store

    def delete(self, name):
        global stores
        stores = list(filter(lambda x: x['name'] != name, stores))


class StoreList(Resource):
    def get(self):
        return stores


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
