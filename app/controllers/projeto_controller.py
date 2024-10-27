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

    processo.projetos.append(ObjectId(projeto.id))
    processo.update({'projetos': processo.projetos, 'data_encerramento': processo.data_encerramento})

    return {
        'message': f'Projeto created successfully with id {projeto.id}',
        'status': 201
    }

def update_projeto(data: dict):
    token = data.headers.get('Authorization').split(' ')[1]

    user_data = decode_jwt_token(token)
    user_id = ObjectId(user_data['user_id'])

    projeto = Projeto.get_by_id(data['id'])
    if not projeto:
        return {'error': 'Projeto does not exists'}, 400

    if projeto.professor != user_id:
        return {'error': 'You do not have permission to update this project'}, 403

    #temq fazer o type check no router antes de mandar pra ca 
    projeto.update(data)

    return {
        'message': f'Projeto updated successfully with id {projeto.id}'
        }, 200

def get_projeto(id: str):
    projeto = Projeto.get_by_id(id)
    return jsonify(projeto.dict())

def get_all_projetos():
    projetos = Projeto.get_all()
    return jsonify([projeto.dict() for projeto in projetos])

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

    return {
        'message': f'Projeto deleted successfully with id {projeto.id}'
        }, 200










    