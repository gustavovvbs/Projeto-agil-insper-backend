from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from models.projeto import Projeto
from database import init_db

class ProcessoSeletivo(BaseModel):
    data_encerramento: date = Field(..., title="Data de Encerramento", description="Data de encerramento do processo seletivo")
    projetos: list[Projeto]

    def __init__(self, data_encerramento: date, projetos: List[Projeto]):
        super().__init__(data_encerramento=data_encerramento, projetos=projetos)
        self.data_encerramento = data_encerramento
        self.projetos = projetos

    def save(self):
        db = init_db()
        db.processos_seletivos.insert_one({
            'data_encerramento': self.data_encerramento,
            'projetos': self.projetos
        })

    def get_all():
        db = init_db()
        processos = db.processos_seletivos.find()
        for processo in processos:
            processo['_id'] = str(processo['_id'])
        return processos

    def get_by_id(id: str):
        db = init_db()
        processo = db.processos_seletivos.find_one({'_id': id})
        processo['_id'] = str(processo['_id'])
        return processo

    def update(self, data):
        db = init_db()
        db.processos_seletivos.update_one({'_id': self.id}, {
            '$set': {
                'data_encerramento': data['data_encerramento'],
                'projetos': data['projetos']
            }
        })
        
    def delete(self):
        db = init_db()
        db.processos_seletivos.delete_one({'_id': self.id})
