from flask import current_app
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class Message:

    @staticmethod
    def create_message(data):
        result = mongo.db.messages.insert_one(data)

        return str(result.inserted_id)

    @staticmethod
    def find_by_id(id):
        return mongo.db.messages.find_one({'_id': ObjectId(id)})

    @staticmethod
    def find_by_sender(sender):
        return mongo.db.messages.find_one({'sender': sender})

    @staticmethod
    def find_by_receiver(receiver):
        return mongo.db.messages.find_one({'receiver': receiver})

    @staticmethod
    def find_by_date(date):
        return mongo.db.messages.find_one({'date': date})

