import os 
from dotenv import load_dotenv  

load_dotenv()

class Config:
    MONGO_URI = os.environ.get('MONGO_URI')
    VECTORSTORE = os.environ.get('VECTORSTORE')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sciconnectinsper@gmail.com'
    MAIL_PASSWORD = os.eviton.get('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'sciconnectinsper@gmail.com'
    SECRET_KEY = os.environ.get('SECRET_KEY')

