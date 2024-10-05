from flask import current_app
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class SelectionProcess:

    @staticmethod
    def create_process(data):
        result = mongo.db.selection_processes.insert_one(data)

        return str(result.inserted_id)

    @staticmethod 
    def find_by_modality(modality):
        return mongo.db.selection_processes.find_one({'modality': modality})

 