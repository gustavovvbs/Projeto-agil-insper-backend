from flask import Flask, request, jsonify, Blueprint
from models import coordenador, estudante, professor, user 
from controllers.auth_controller import register_user, login_user
from utils.auth_decorator import role_required


auth_routes = Blueprint('auth', __name__)


@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = register_user(data)

    return response

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = login_user(data)

    return response 