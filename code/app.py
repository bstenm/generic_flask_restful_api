from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
import credentials

app = Flask(__name__)
app.secret_key = credentials.jwt_key
api = Api(app)

# create a new endpoint "/auth"
jwt = JWT(app, authenticate, identity)

stores = []


class Store(Resource):

    @jwt_required()
    def get(self, name):
        matches = filter(lambda store: store["name"] == name, stores)
        store = next(matches, None)
        return {"store": store}

    def post(self, name):
        matches = filter(lambda store: store["name"] == name, stores)
        if next(matches, None):
            return {"message": f"A store with name '{name}' already exists"}, 400

        data = request.get_json()
        store = {"name": name, "city": data["city"]}
        stores.append(store)
        return store, 201


class StoreList(Resource):
    def get(self):
        return stores


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

app.run(port=5000, debug=True)
