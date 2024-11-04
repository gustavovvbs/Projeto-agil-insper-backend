from flask import request, Blueprint
from controllers.auth_controller import register_user, login_user

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