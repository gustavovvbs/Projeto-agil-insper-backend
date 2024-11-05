
from flask import Flask, request, jsonify, Blueprint
from models import coordenador, estudante, professor, user 
from controllers.auth_controller import register_user, login_user, create_token_and_send_email, change_password, show_user_info_by_token


auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register_user(data)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    return login_user(data)

@auth_routes.route("/esqueci-senha/<email>", methods=["POST"])
def request_password_reset(email):
    return create_token_and_send_email(email)

@auth_routes.route("/recuperar/<token>", methods=["GET","POST"])
def reset_password(token):
    if request.method == "POST":
        data = request.get_json()
        return change_password(token, data)
    return show_user_info_by_token(token)