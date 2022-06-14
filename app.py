
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
import os

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret-key'
uri = os.environ.get("DATABASE_URL",  'sqlite:///data.db')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWT(app, authenticate, identity) # /auth

api = Api(app)

items = []

        
api.add_resource(Item, "/items/<string:name>") # http://127.0.0.1:5000/items/chairs
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items/")
api.add_resource(StoreList, "/stores/")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    
    app.run(port=5000, debug=True)