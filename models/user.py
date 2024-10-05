from flask import current_app
from app import mongo 
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User:

    @staticmethod
    def create_user(data):
        data['password'] = generate_password_hash(data['password'])
        result = mongo.db.users.insert_one(data)

        return str(result.inserted_id)

    @staticmethod 
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def find_by_id(id):
        return mongo.db.users.find_one({'_id': ObjectId(id)})

    @staticmethod
    def check_password(user_password, password):
        return check_password_hash(user_password, password)

        