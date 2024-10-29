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

@projeto_routes.route('/<id>', methods=['PUT'])
@role_required(['coordenador', 'professor'])
def update(id):
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

    #ver c o thiagao se eh suave deixa essa autenticacao aq pela peculiaridade dessa checagem de ownnership
    data = request.get_json()
    token = request.headers.get('Authorization').split(' ')[1]
    data['token'] = token

    # user_data = decode_jwt_token(token)

    # user_id = ObjectId(user_data['user_id'])

    # if user_data['role'] == 'professor' and projeto.professor != user_id:
    #     return {'error': 'You do not have permission to update this project'}, 40
    # #se for coordenador ou o dono do projeto pd editar
    # if user_data['role'] == 'coordenador' or projeto.professor == user_id:
    response = update_projeto(data, id)
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

