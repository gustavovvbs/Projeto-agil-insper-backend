from pymongo import MongoClient
from config import Config 

mongo = MongoClient(Config.MONGO_URI)

def init_db():
    db = mongo['agil-db']
    return db

def init_db_temporary_tokens():
    db = mongo["agil-db-temporary-tokens"]
    return db
