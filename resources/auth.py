from flask import Blueprint, request, jsonify 
from app import mongo 
from models.user import User 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing fields'}), 400

    if User.find_by_email(data['email']):
        return jsonify({'message': 'Email already registered'}), 400

    user_id = User.create_user(data)
    return jsonify({'User registered': user_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    if user and User.check_password(user['password'], data['password']):
        access_token = create_access_token(identity=str(user['_id']), additional_claims={'role': user['role']})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

