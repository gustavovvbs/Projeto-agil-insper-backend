from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from database import init_db
from bson import ObjectId

class ProcessoSeletivo(BaseModel):
    id: Optional[str] = None
    titulo: str = Field("Processo não nomeado", title="Título", description="Título do processo seletivo")
    data_encerramento: datetime = Field(..., title="Data de Encerramento", description="Data de encerramento do processo seletivo")
    projetos: Optional[List[str]] = Field(None, title="Projetos", description="Projetos do processo seletivo")

    def __init__(self, data_encerramento: datetime, projetos: Optional[List[str]] = None, id: Optional[str] = None):
        super().__init__(data_encerramento=data_encerramento, projetos=projetos)
  
    def save(self):
        db = init_db()
        #convertendo pq o bson n encoda
        if datetime.now() > self.data_encerramento:
            raise ValueError("Data de encerramento inválida")

        self.id = str(db.processos_seletivos.insert_one({
            'data_encerramento': self.data_encerramento,
            'projetos': self.projetos
        }).inserted_id)


    @staticmethod
    def get_all():
        db = init_db()
        processos = list(db.processos_seletivos.find())
        for processo in processos:
            processo['id'] = str(processo['_id'])
            #popando o _id pq n ta no modelo
            processo.pop('_id')

        return processos

    @classmethod
    def get_by_id(cls, id: str):
        db = init_db()
        processo = db.processos_seletivos.find_one({'_id': ObjectId(id)})
        processo['id'] = str(processo['_id'])
        #popando o _id pq n ta no modelo
        processo.pop('_id')
        return cls(**processo) if processo else None

    @staticmethod
    def update(data):
        db = init_db()
        db.processos_seletivos.update_one({'_id': ObjectId(data['id'])}, {
            '$set': {
                'data_encerramento': data['data_encerramento'],
                'projetos': data['projetos']
            }
        })
        
    def delete(self):
        db = init_db()
        db.processos_seletivos.delete_one({'_id': self.id})
