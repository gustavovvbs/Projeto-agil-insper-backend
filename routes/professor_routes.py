
from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor
from controllers.professor_controller import get_by_id, get_all, get_projects_by_professor, get_project_by_id, get_applications_by_project_id, get_aplicacao
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

@professor_routes.route("/<id_professor>/projeto", methods=["GET"])
@role_required(["professor"])
def get_all_projects(id_professor):
    response = get_projects_by_professor(id_professor)

    return response

@professor_routes.route("/<id_professor>/projeto/<id_projeto>", methods=["GET"])
@role_required(["professor"])
def get_project(id_projeto):
    response = get_project_by_id(id_projeto)

    return response

@professor_routes.route("/projeto/<id_projeto>/aplicacoes", methods=["GET"])
@role_required(["professor"])
def get_project_applications(id_projeto):
    response = get_applications_by_project_id(id_projeto)
    
    return response


@professor_routes.route("<id_professor>/projetos/<id_projeto>/aplicacoes/<id_aplicacao>", methods=["GET"])
@role_required(["professor"])
def get_application(id_projeto, id_aplicacao):
    response = get_aplicacao(id_aplicacao)
    return response
