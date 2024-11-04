from pymongo import MongoClient
from config import Config 

mongo = MongoClient(Config.MONGO_URI)

def init_db():
    db = mongo['agil-db']
    return db