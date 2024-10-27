from utils.matchmaking import respond_query
from utils.auth_decorator import role_required
from flask import request, jsonify, Blueprint

matchmaking_routes = Blueprint('matchmaking', __name__)

@matchmaking_routes.route('/query', methods=['POST'])
@role_required(['estudante'])
def query():
    data = request.get_json()
    response = respond_query(**data)
    response = [x.dict() for x in response]
    return response