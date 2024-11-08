from flask import Blueprint, request, jsonify
from controllers.aplicacao_controller import create_aplicacao, get_all_aplicacoes, get_aplicacao_by_professor, check_processo_date, get_aplicacao_by_projeto,aprova_aplicacao,reprova_aplicacao
from utils.jwt_auth import decode_jwt_token
from utils.auth_decorator import role_required 

aplicacao_routes = Blueprint('aplicacao', __name__)

@aplicacao_routes.route('/', methods=['POST'])
@role_required(['estudante'])
def create():
    response = create_aplicacao(request)
    return response

@aplicacao_routes.route('/' , methods=['GET'])
@role_required(['coordenador'])
def get_all():
    """
        Retorna todas as aplicacoes.
    """
    aplicacoes = get_all_aplicacoes()
    return jsonify(aplicacoes)

#esse endpoint aq o cara se identifica pelo jwt p pegar as aplicacoes dele, tem que ter outro p filtrar por professor na visao do coordenador talvez
@aplicacao_routes.route('/professor', methods=['GET'])
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
    
    aplicacoes = get_aplicacao_by_professor(payload['user_id'])
    date_check = check_processo_date(aplicacoes)
    if not date_check:
        return {"error": "Proccess still open"}, 400 
    
    if isinstance(date_check, dict):
        return jsonify(date_check), 400

    return jsonify(aplicacoes), 200

@aplicacao_routes.route('/projeto/<string:id_projeto>', methods=['GET'])
def get_by_projeto(id_projeto):
    aplicacoes = get_aplicacao_by_projeto(id_projeto)
    date_check = check_processo_date(aplicacoes)
    if not date_check:
        return {"error": "Proccess still open"}, 400 
    
    if isinstance(date_check, dict):
        return jsonify(date_check), 400

    return jsonify(aplicacoes), 200

@aplicacao_routes.route('/<string:id_aplicacao>/projeto/<string:id_projeto>' , methods=['PUT'])
@role_required(['professor'])
def end_application_process(id_aplicacao,id_projeto):
    reprova_aplicacao(id_projeto)
    aprova_aplicacao(id_aplicacao)
    return {'message': 'Success'}, 200

    

