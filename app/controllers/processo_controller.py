from models.processo_seletivo import ProcessoSeletivo
from datetime import date
from utils.auth_decorator import role_required


def create_processo(data: dict):
    processo = ProcessoSeletivo(**data)
    processo.save()
    return {"message": f"Processo created successfully with id {processo.id}"}, 201

def update_processo(data: dict):
    processo = ProcessoSeletivo.get_by_id(data['id'])
    #criando outra instancia p checar a tipagem
    new_processo = ProcessoSeletivo(**data).dict()
    new_processo['id'] = data['id']
    processo.update(new_processo)

    updated_processo = ProcessoSeletivo.get_by_id(data['id'])
    updated_processo = updated_processo.dict()
    updated_processo['id'] = data['id']

    return {'message': f'Processo updated successfully with id {data["id"]}'}, 201

def get_all_processos():
    processos = ProcessoSeletivo.get_all()
    return processos

def get_processo_by_id(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    return processo

def delete_processo(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    processo.delete()
    return {'message': f'Processo deleted successfully with id {id}'}, 200





