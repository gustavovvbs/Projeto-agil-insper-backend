import os 
from dotenv import load_dotenv  

load_dotenv()

class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    VECTORSTORE = os.environ.get('VECTORSTORE')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    EMAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "your_mail@gmail.com"
    MAIL_PASSWORD = "your_email_password"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True