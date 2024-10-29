from models.processo_seletivo import ProcessoSeletivo
from datetime import date
from utils.auth_decorator import role_required


def create_processo(data: dict):
    processo = ProcessoSeletivo(**data)
    processo.save()
    return {"message": f"Processo created successfully with id {processo.id}"}, 201

def update_processo_by_id(data: dict, id: str):
    data['id'] = id
    response = ProcessoSeletivo.update(data)

    return response

def get_all_processos():
    processos = ProcessoSeletivo.get_all()
    processos = [processo.dict() for processo in processos]
    return processos

def get_processo_by_id(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    return processo

def delete_processo(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    processo.delete()
    return {'message': f'Processo deleted successfully with id {id}'}, 200





