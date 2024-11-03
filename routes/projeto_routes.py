from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from controllers.projeto_controller import create_projeto, update_projeto, get_projeto, get_all_projetos, delete_projeto, get_projetos_by_processo, check_processo_date, get_projeto_by_professor
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

    return jsonify(response[0]), response[1]

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

    response = update_projeto(data, id)
    return jsonify(response)

@projeto_routes.route('/<id>', methods=['GET'])
def get(id: str):
    """ 
        Retorna um projeto pelo id. 
        Permissionamento: qualquer um
    """

    response = get_projeto(id)

    return jsonify(response[0]), response[1]

@projeto_routes.route('/', methods=['GET'])
def get_all():
    """ 
        Retorna todos os projetos. 
        Permissionamento: qualquer um
    """

    response = get_all_projetos()

    return jsonify(response)

@projeto_routes.route('/processo/<id>', methods=['GET'])
@role_required(['coordenador'])
def get_by_processo(id):
    """ 
        Retorna todos os projetos de um processo seletivo. 
        Permissionamento: coordenador e professor
    """

  
    response = get_projetos_by_processo(id)

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

@projeto_routes.route('/professor', methods=['GET'])
@role_required(['professor'])
def get_by_professor():
    """
        Retorna todas as aplicacoes de um professor.
        Permissionamento: professor
    """
    token = request.headers.get('Authorization').split(' ')[1]
    payload = decode_jwt_token(token)
    if payload['role'] != 'professor':
        return jsonify({"error": "Unauthorized."}), 401
    
    aplicacoes = get_projeto_by_professor(payload['user_id'])
    return jsonify(aplicacoes)