from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from database import init_db
from bson import ObjectId

class ProcessoSeletivo(BaseModel):
    id: Optional[str] = None
    titulo: str = Field("Processo não nomeado", title="Título", description="Título do processo seletivo")
    data_encerramento: datetime = Field(..., title="Data de Encerramento", description="Data de encerramento do processo seletivo")
    projetos: Optional[List[str]] = Field([], title="Projetos", description="Projetos do processo seletivo")

  
    def save(self):
        db = init_db()
        #convertendo pq o bson n encoda
        if datetime.now() > self.data_encerramento:
            raise ValueError("Data de encerramento inválida")

        self.id = str(db.processos_seletivos.insert_one({
            'data_encerramento': self.data_encerramento,
            'projetos': self.projetos,
            'titulo': self.titulo
        }).inserted_id)

        if not self.id:
            return {"message": "Error saving Processo Seletivo"}, 400

        return {"message": f"Processo Seletivo saved successfully with id {self.id}"}, 201


    @classmethod
    def get_all(cls):
        db = init_db()
        processos = list(db.processos_seletivos.find())
        if not processos:
            return None
        for processo in processos:
            processo['id'] = str(processo['_id'])
            #popando o _id pq n ta no modelo
            processo.pop('_id')


        processos = [cls(**processo) for processo in processos]
        return processos

    @classmethod
    def get_by_id(cls, id: str):
        db = init_db()
        processo = db.processos_seletivos.find_one({'_id': ObjectId(id)})
        if not processo:
            return None
        processo['id'] = str(processo['_id'])
        #popando o _id pq n ta no modelo
        processo.pop('_id')

        #p garantir em caso de por algum motivo ter salvo como objectid
        for projeto in processo['projetos']:
            projeto = str(projeto)

        return cls(**processo) if processo else None

    @classmethod
    def update(cls, data):
        db = init_db()

        processo = cls.get_by_id(data['id'])
        if not processo:
            return {"message": "Processo Seletivo not found"}, 404

        update_data = {k: v for k, v in data.items() if v is not None and k != 'id'}

        response = db.processos_seletivos.update_one({'_id': ObjectId(data['id'])}, {
            '$set': update_data
        })

        if response.modified_count == 0:
            return {"message": "No changes were made"}, 400

        return {"message": f"Processo Seletivo updated successfully with id {data['id']}"}, 201
        
    def delete(self):
        db = init_db()
        db.processos_seletivos.delete_one({'_id': self.id})
