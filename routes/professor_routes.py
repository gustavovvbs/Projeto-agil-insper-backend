from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor
from controllers.professor_controller import get_by_id, get_all
from bson import ObjectId
from flask import Blueprint, request, jsonify

professor_routes = Blueprint('professor', __name__)

@professor_routes.route('/<id>', methods=['GET'])
def get_professor_by_id(id):
    response = get_by_id(id)

    return response

@professor_routes.route('/', methods=['GET'])
def get_all_professores():
    response = get_all()

    return response

# @professor_routes.route()