from flask import Flask, request, jsonify
import hashlib
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime 
import os 
from dotenv import load_dotenv
import uvicorn 
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

client = MongoClient(os.getenv('MONGO_URI'))
db = client['agil-db']
users_colletion = db['users']

@app.route('/api/users', methods=['POST'])
def register():
    new_user = request.get_json()

    #criando o hash da senha 
    new_user['password'] = hashlib.sha256(new_user['password'].encode()).hexdigest()

    doc = users_collection.find_one({'username': new_user['username']})

    if not doc:
        user_collection.insert_one(new_user)
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    else:
        return jsonify({'message': 'Usuário já existe'}), 400

@app.route('/api/users', methods=['GET'])
def login():
    user = request.get_json()

    user_db = user_collection.find_one({'username': user['username']})

    if user_db:
        encoded_password = hashlib.sha256(user['password'].encode()).hexdigest()
        if encoded_password == user_db['password']:
            access_token = create_access_token(identity=user['username'], expires_delta=datetime.timedelta(days=1))
            return jsonify({'access_token': access_token}), 200
        
    return jsonify({'message': 'Usuário ou senha inválidos'}), 401

@app.route('/api/users', methods=['PUT'])
@jwt_required()
def update():
    user = request.get_json()
    user['username'] = get_jwt_identity()

    user_collection.update_one({'username': user['username']}, {'$set': user})

