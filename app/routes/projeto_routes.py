from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor
from controllers.projeto_controller import create_projeto, update_projeto, get_projeto, get_all_projetos, delete_projeto
from bson import ObjectId
from flask import Blueprint, request, jsonify

projeto_routes = Blueprint('projeto', __name__)

@projeto_routes.route('/', methods=['POST'])
@role_required(['coordenador', 'professor'])
def create():
    """ 
        Cria um projeto novo. 
        Permissionamento: coordenador e professor

        formato: 
        {
            "processo_seletivo": "id do processo seletivo",
            "professor": "id do professor",
            "temas": ["tema 1", "tema 2"],
            "descricao": "descricao do projeto"
        }
    """

    data = request.get_json()
    response = create_projeto(data)

    return jsonify(response)

@projeto_routes.route('/', methods=['PUT'])
@role_required(['coordenador', 'professor'])
def update():
    """ 
        Atualiza um projeto existente. 
        Permissionamento: coordenador e professor

        formato: 
        {
            "processo_seletivo": "id do processo seletivo",
            "professor": "id do professor",
            "temas": ["tema 1", "tema 2"],
            "descricao": "descricao do projeto"
        }
    """

    data = request.get_json()
    try:
        type_check = Projeto(data['processo_seletivo'], data['professor'], data['temas'], data['descricao'])
    except TypeError:
        return jsonify({"error": "Invalid data format"}), 400
    
    projeto_data = type_check.dict()
    response = update_projeto(projeto_data)

    return jsonify(response)

@projeto_routes.route('/<id>', methods=['GET'])
def get(id: str):
    """ 
        Retorna um projeto pelo id. 
        Permissionamento: qualquer um
    """

    response = get_projeto(id)

    return jsonify(response)

@projeto_routes.route('/', methods=['GET'])
def get_all():
    """ 
        Retorna todos os projetos. 
        Permissionamento: qualquer um
    """

    response = get_all_projetos()

    return jsonify(response)

@projeto_routes.route('/', methods=['DELETE'])
@role_required(['coordenador', 'professor'])
def delete():
    """ 
        Deleta um projeto existente. 
        Permissionamento: coordenador e professor

        formato: 
        {
            "id": "id do projeto"
        }
    """

    data = request.get_json()
    response = delete_projeto(data)

    return jsonify(response)

