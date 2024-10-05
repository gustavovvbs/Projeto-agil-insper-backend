import os 
from datetime import timedelta 
from dotenv import load_dotenv 

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET = os.getenv('JWT_SECRET')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    