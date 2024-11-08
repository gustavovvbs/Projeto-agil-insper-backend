from utils.jwt_auth import decode_jwt_token
from models.projeto import Projeto 
from models.processo_seletivo import ProcessoSeletivo
from bson import ObjectId
import datetime

def create_projeto(data: dict):
    processo = ProcessoSeletivo.get_by_id(data['processo_seletivo'])

    if not processo:
        return {'error': 'Processo does not exists'}, 400
    if len(data) != 6:
        return {'error': 'Bad Request'}, 409 
    temas = data.get("temas", [])
    aplicacoes = data.get("aplicacoes", [])
    if isinstance(temas, str):
        temas = [temas]
    if isinstance(aplicacoes, str):
        aplicacoes = [aplicacoes]
    projeto = Projeto(
        processo_seletivo=data.get('processo_seletivo'),
        titulo=data.get('titulo'),
        professor=data.get("professor"),
        temas=temas,
        descricao=data.get("descricao"),
        aplicacoes=aplicacoes
        )
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
    if not projeto:
        return {'error': 'Projeto does not exists'}, 400
        
    return projeto.dict(), 200

def get_projeto_by_professor(id_professor: str):
    projeto = Projeto.get_all_by_professors(id_professor=id_professor)
    if not projeto:
        return {'error': 'Projeto does not exists'}, 400
        
    return [p.dict() for p in projeto]

def get_projetos_by_processo(id: str):
    projetos = Projeto.get_by_processo(id)
    if not projetos:
        return {'error': 'No projects found for this process'}, 404

    if projetos == None:
        return {'error': 'Processo does not exists'}, 400
    
    projetos = [projeto.dict() for projeto in projetos]

    return projetos

def get_all_projetos():
    projetos = Projeto.get_all()
    projetos = [projeto.dict() for projeto in projetos]
    return projetos

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

def get_aplicacao_by_projeto(id: str):
    aplicacoes = Projeto.get_by_professor(id)
    return [aplicacao.dict() for aplicacao in aplicacoes]

def check_processo_date(data: dict):
    processo = ProcessoSeletivo.get_by_id(data[0]['processo_seletivo'])
    if not processo:
        return {'error': 'Processo Seletivo does not exist'}, 400

    if datetime.datetime.now() < processo.data_encerramento:
        return False

    return True
