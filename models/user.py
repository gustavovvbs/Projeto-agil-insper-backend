from database import init_db
from bson import ObjectId

db = init_db()

class User:
    def __init__(self, email, password, role):
        self.email = email 
        self.password = password 
        self.role = role 

    def save(self):
        user_id = db.users.insert_one({
            'email': self.email,
            'password': self.password,
            'role': self.role
        }).inserted_id

        return user_id

    @staticmethod 
    def find_by_email(email):
        user = db.users.find_one({"email": email})
        return user if user else None

    @staticmethod
    def get_by_id(id):
        user = db.users.find_one({"_id": ObjectId(id)})
        return user if user else None

    @staticmethod
    def put(id, email, password, role):
        user = db.users.update_one({"_id": ObjectId(id)},{'$set':{'email': email, 'password': password, 'role': role}})
        return user if user else None
    
    @staticmethod
    def delete(email):
        user = db.users.delete_one({"email": email})
        return user if user else None