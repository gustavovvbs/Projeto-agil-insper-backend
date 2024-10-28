from flask import Flask, Blueprint, request, jsonify
from models.processo_seletivo import ProcessoSeletivo
from controllers.processo_controller import create_processo, get_processo_by_id, get_all_processos, update_processo, delete_processo
from utils.auth_decorator import role_required

processo_routes = Blueprint('processo', __name__)

@processo_routes.route('/', methods=['POST'])
@role_required('coordenador')
def create():
    """
        Cria um processo seletivo novo.
        Permissionamento: coordenador

        formato:
        {
            "data_encerramento": "YYYY-MM-DD",
            "projetos": ["id do projeto 1", "id do projeto 2"] | [] (a requisicao p criar quase sempre n vai ter nd pq os professores vao botar dps),
            "titulo": "titulo do processo",

        }
    """

    data = request.get_json()
    response = create_processo(data)

    return jsonify(response.dict())

@processo_routes.route('/<id>', methods=['GET'])
def get_by_id(id):
    id = request.args.get('id')
    response = get_processo(id)

    return jsonify(response.dict())

@processo_routes.route('/', methods=['GET'])
def get_all():
    response = get_all_processos()

    return jsonify(response)

@processo_routes.route('/<id>', methods=['PUT'])
@role_required('coordenador')
def update(id):
    data = request.get_json()
    data['id'] = id
    response = update_processo(data)

    return jsonify(response[0]), response[1]

@processo_routes.route('/', methods=['DELETE'])
@role_required('coordenador')
def delete():
    id = request.args.get('id')
    response = delete_processo(id)

    return jsonify(response.dict())

