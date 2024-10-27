from models.processo_seletivo import ProcessoSeletivo
from datetime import date
from utils.auth_decorator import role_required


def create_processo(data: dict):
    processo = ProcessoSeletivo(**data)
    processo.save()
    return processo

def editar_processo(data: dict):
    processo = ProcessoSeletivo.get_by_id(data['id'])
    #criando outra instancia p checar a tipagem
    new_processo = ProcessoSeletivo(**data).dict()
    processo.update(**new_processo)
    return processo

def get_all_processos():
    processos = ProcessoSeletivo.objects()
    return processos

def get_processo_by_id(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    return processo





