import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel  

class UserRegister(Resource):
    
    request = reqparse.RequestParser()
    # For username
    request.add_argument('username', 
        type=str,
        required=True,
        help = "Username required!!"
    )
    # For Password
    request.add_argument('password', 
        type=str,
        required=True,
        help = "Password required!!"
    )
    
    def post(self):
        # fetch data from json
        data = UserRegister.request.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"Messsage": "Username {0} already exists".format(data['username'])}, 401
        
        user = UserModel(**data)
        user.save_to_db()
        
        return {"Message":"User %s created successfully!!"%data['username']}, 201
        
        