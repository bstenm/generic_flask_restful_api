from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from user import UserRegister
from store import Store, StoreList
from security import authenticate, identity
import credentials

app = Flask(__name__)
app.secret_key = credentials.jwt_key
api = Api(app)

# create a new endpoint '/auth'
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
