from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_auth import create_jwt_token
from models.user import User 
from models.estudante import Estudante
from models.coordenador import Coordenador
from models.professor import Professor
from flask import request, jsonify, Blueprint
from database import init_db

db = init_db()

def register_user(data):
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    curso = data.get('curso')
    semestre = data.get('semestre')
    nome = data.get('nome')
    
    if not email or not password or not role or not nome:
        return jsonify({"error": f"missing fields"}), 400

    if User.find_by_email(email):
        return jsonify({"error": "User already exists"}), 400
    
    if role == 'estudante':
        estudante = Estudante(nome, email, curso, semestre)
        estudante.save()
    elif role == 'coordenador':
        coordenador = Coordenador(nome, email)
        coordenador.save()
    
    hashed_password = generate_password_hash(password)
    user = User(email, hashed_password, role)
    user_id = user.save()



    return jsonify({"message": "User registered successfully"}), 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')

    user_record = User.find_by_email(email)
    if not user_record:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user_record['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    #ver oq fzer p n criar um token novo a cada login
    print(user_record)
    token = create_jwt_token(str(user_record["_id"]), user_record['role'])

    #<----------- popo o id do user do dict q vem das collection especifica e adiciono o role_id p ficar mais claro ql eh de role e geral-->
    if user_record["role"] == "estudante":
        role_specific_data = db.estudantes.find_one({"email": user_record["email"]})
        role_specific_data["role_id"] = str(role_specific_data["_id"])
        role_specific_data.pop("_id")
    elif user_record["role"] == "coordenador":
        role_specific_data = db.coordenadores.find_one({"email": user_record["email"]})
        role_specific_data["role_id"] = str(role_specific_data["_id"])
        role_specific_data.pop("_id")
    elif user_record["role"] == "professor":
        role_specific_data = db.professores.find_one({"email": user_record["email"]})
        role_specific_data["role_id"] = str(role_specific_data["_id"])
        role_specific_data.pop("_id")

    return {
        "message": "User logged in successfully",
        "token": token,
        "user_id": str(user_record["_id"]),
        "user": {
            "email": user_record["email"],
            "role": user_record["role"],
            **role_specific_data
        },
        "status": 200
    }

    