import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password", type=str, required=True)

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "Username is already taken"}, 400

        user = UserModel(None, data["username"], data["password"])
        try:
            user = user.save_user()
        except:
            return {"message": "An error occured while creating a new user"}, 500

        return {"data": {"id": user.id, "username": user.username}, "message": "User created successfully"}, 201
