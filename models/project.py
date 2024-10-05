from flask import current_app
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class Project:

    @staticmethod
    def create_project(data):
        result = mongo.db.selection_processes.insert_one(data)

        return str(result.inserted_id)

    @staticmethod
    def find_by_professor(professor_id):
        return mongo.db.selection_processes.find_one({'professor_id': ObjectId(professor_id)})

    @staticmethod
    def find_by_id(id):
        return mongo.db.selection_processes.find_one({'_id': ObjectId(id)})

    @staticmethod 
    def find_by_modality(modality):
        return mongo.db.selection_processes.find_one({'modality': modality})

    @staticmethod
    def find_by_course(course):
        return mongo.db.selection_processes.find_one({'course': course})

    @staticmethod
    def find_by_period(period):
        return mongo.db.selection_processes.find_one({'period': period})