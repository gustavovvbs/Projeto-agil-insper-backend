from flask import current_app
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class Application:

    @staticmethod
    def create_application(data):
        result = mongo.db.applications.insert_one(data)

        return str(result.inserted_id)

    @staticmethod
    def find_by_id(id):
        return mongo.db.applications.find_one({'_id': ObjectId(id)})

    @staticmethod
    def find_by_student(student):
        return mongo.db.applications.find_one({'student': student})

    @staticmethod
    def find_by_process(process):
        return mongo.db.applications.find_one({'process': process})

    @staticmethod
    def find_by_status(status):
        return mongo.db.applications.find_one({'status': status})

