from models.processo_seletivo import ProcessoSeletivo

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
    if not processos:
        return {'error': 'No processos found'}, 404
    processos = [processo.dict() for processo in processos]
    return processos

def get_processo_by_id(id: str):
    response = ProcessoSeletivo.get_by_id(id)
    if not response:
         return {'error': 'Processo not found'}, 404
         

    return response.dict(), 200

def delete_processo(id: str):
    processo = ProcessoSeletivo.get_by_id(id)
    if not processo:
        return {'error': 'Processo not found'}, 404
    processo.delete()
    return {'message': f'Processo deleted successfully with id {id}'}, 200





