from flask import Flask, Blueprint, request, jsonify
from models import processo
from controllers.processo_controller import create_processo, get_processo, get_processos, update_processo, delete_processo
from utils.auth_decorator import role_required

processo_routes = Blueprint('processo', __name__)

@processo_routes.route('/processo', methods=['POST'])
@role_required('coordenador')
def create():
    data = request.get_json()
    response = create_processo(data)

    return jsonify(response.dict())

@processo_routes.route('/processo', methods=['GET'])
def get_by_id():
    id = request.args.get('id')
    response = get_processo(id)

    return jsonify(response.dict())

@processo_routes.route('/processo', methods=['GET'])
def get_all():
    response = get_processos()

    return jsonify([p.dict() for p in response])

@processo_routes.route('/processo', methods=['PUT'])
@role_required('coordenador')
def update():
    data = request.get_json()
    response = update_processo(data)

    return jsonify(response.dict())

@processo_routes.route('/processo', methods=['DELETE'])
@role_required('coordenador')
def delete():
    id = request.args.get('id')
    response = delete_processo(id)

    return jsonify(response.dict())

