
from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor
from controllers.professor_controller import get_by_id, get_all, get_projects_by_professor, get_project_by_id, get_applications_by_project_id
from controllers.aplicacao_controller import get_aplicacao
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

@professor_routes.route("/projetos/professor/<id>", methods=["GET"])
@role_required(["professor"])
def get_all_projects(id):
    response = get_projects_by_professor(id)

    return response

@professor_routes.route("/projetos/<id>", methods=["GET"])
@role_required(["professor"])
def get_project(id):
    response = get_project_by_id(id)

    return response

@professor_routes.route("/projetos/<id>/aplicacoes", methods=["GET"])
@role_required(["professor"])
def get_project_applications(id):
    response = get_applications_by_project_id(id)
    
    return response


@professor_routes.route("/projetos/<id>/aplicacoes/<id_aplicacao>", methods=["GET"])
@role_required(["professor"])
def get_application(id, id_aplicacao):
    response = get_aplicacao(id_aplicacao)
    return response
