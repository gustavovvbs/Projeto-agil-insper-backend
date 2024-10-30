from utils.auth_decorator import role_required
from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto 
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor
from bson import ObjectId

def create_projeto(data: dict):
    processo = ProcessoSeletivo.get_by_id(data['processo_seletivo'])

    if not processo:
        return {'error': 'Processo does not exists'}, 400

    projeto = Projeto(**data)
    projeto.save()

    processo.projetos.append(str(projeto.id))

    processo.update({'projetos': processo.projetos, 'data_encerramento': processo.data_encerramento, 'id': projeto.processo_seletivo})

    return {'message': f'Projeto created successfully with id {projeto.id}'}, 201

def update_projeto(data: dict, id: str):
    token = data['token']
    payload = decode_jwt_token(token)

    if payload['role'] == 'professor' and projeto.professor != payload['user_id']:
        return {'error': 'You do not have permission to update this project'}, 403

    if payload['role'] != 'coordenador':
        return {'error': 'You do not have permission to update this project'}, 403

    projeto = Projeto.get_by_id(id)
    if not projeto:
        return {'error': 'Projeto does not exists'}, 400

    
    data['id'] = id
    response = projeto.update_by_id(data)

    return response

def get_projeto(id: str):
    projeto = Projeto.get_by_id(id)
    return jsonify(projeto.dict())

def get_projetos_by_processo(id: str):
    projetos = Projeto.get_by_processo(id)
    if not projetos:
        return {'error': 'Processo does not exists'}, 400
    
    projetos = [projeto.dict() for projeto in projetos]
    return projetos, 200

def get_all_projetos():
    projetos = Projeto.get_all()
    projetos = [projeto.dict() for projeto in projetos]
    return projetos, 200

def delete_projeto(data: dict):
    token = data.headers.get('Authorization').split(' ')[1]

    user_data = decode_jwt_token(token)
    user_id = ObjectId(user_data['user_id'])

    projeto = Projeto.get_by_id(data['id'])
    if not projeto:
        return {'error': 'Projeto does not exists'}, 400

    if projeto.professor != user_id or user_data['role'] != 'coordenador':
        return {'error': 'You do not have permission to delete this project'}, 403

    projeto.delete()

    return {'message': f'Projeto deleted successfully with id {projeto.id}'} , 200










    