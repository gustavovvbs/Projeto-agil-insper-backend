from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt_auth import create_jwt_token
from models.user import User 
from models.estudante import Estudante
from models.coordenador import Coordenador
from models.professor import Professor
from flask import request, jsonify, Blueprint
from database import init_db, init_db_temporary_tokens
from mail import mail
from flask_mail import Message
from datetime import datetime, timedelta
db = init_db()

def register_user(data):
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    curso = data.get('curso')
    semestre = data.get('semestre')
    nome = data.get('nome')
    area_pesquisa = data.get('area_pesquisa')
    descricao = data.get('descricao')
    
    if not email or not password or not role or not nome:
        return {}

    if User.find_by_email(email):
        return jsonify({"error": "User already exists"}), 400
    
    if role == 'estudante':
        estudante = Estudante(nome, email, curso, semestre)
        estudante.save()
    elif role == 'coordenador':
        coordenador = Coordenador(nome, email)
        coordenador.save()
    if role == 'professor':
        professor = Professor(nome, email, area_pesquisa, descricao)
        professor.save()
    
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

def create_token_and_send_email(id):
    user = User.get_by_id(id)  
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    email = user["email"]  
    
    token = create_jwt_token(str(user["_id"]), user['role'], expires_in=3600) 
    
    reset_url = f"http://localhost:8000/auth/recuperar/{token}" 
    
    try:
        mail.send_message(
            subject="Recuperação de Senha",
            recipients=[email],
            body=f"""
            Você solicitou a recuperação de senha.
            
            Para redefinir sua senha, clique no link abaixo:
            {reset_url}
            
            Este link expira em 1 hora.
            
            Se você não solicitou esta alteração, ignore este email.
            """
        )
        
        # Store token in temporary collection with expiration
        temp_db = init_db_temporary_tokens()
        temp_db.reset_tokens.insert_one({
            "user_id": user["_id"],
            "token": token,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=1)
        })
        
        return jsonify({
            "message": "Password reset instructions sent to your email",
            "email": email
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

def change_password(token, data):
    if not data or 'new_password' not in data:
        return jsonify({"error": "New password is required"}), 400

    temp_db = init_db_temporary_tokens()
    token_record = temp_db.reset_tokens.find_one({
        "token": token,
        "expires_at": {"$gt": datetime.utcnow()}
    })
    
    if not token_record:
        return jsonify({"error": "Invalid or expired reset token"}), 400
        
    try:
        hashed_password = generate_password_hash(data["new_password"])
        if User.update_password(str(token_record["user_id"]), hashed_password):
            # Delete used token
            temp_db.reset_tokens.delete_one({"_id": token_record["_id"]})
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update password"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to update password: {str(e)}"}), 500