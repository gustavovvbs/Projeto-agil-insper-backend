from pydantic import BaseModel, Field 
from typing import List, Optional
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor 
from bson import ObjectId
from database import init_db

class Projeto(BaseModel):
    id: Optional[str] = None
    processo_seletivo: Optional[str] = Field(..., title="Processo Seletivo", description="Processo Seletivo's ObjectId")
    titulo: str = Field('Projeto não nomeado', title="Título", description="Título do projeto")
    professor: Optional[str] = Field(..., title="Professor", description="Professor's ObjectId")
    temas: List[str]
    descricao: Optional[str]
    aplicacoes: Optional[List[str]] = Field([], title="Aplicações", description="Aplicações do projeto")

    def save(self):
        db = init_db()
        self.id = str(db.projetos.insert_one({
            'processo_seletivo': self.processo_seletivo,
            'professor': self.professor,
            'temas': self.temas,
            'descricao': self.descricao,
            'titulo': self.titulo,
        }).inserted_id)

    @classmethod
    def get_by_id(cls, id: str):
        db = init_db()
        projeto = db.projetos.find_one({'_id': ObjectId(id)})
        if not projeto:
            return None
        projeto['id'] = str(projeto['_id'])
        projeto.pop('_id')
        return cls(**projeto)

    @classmethod
    def get_all(cls):
        db = init_db()
        projetos = list(db.projetos.find())
        for projeto in projetos:
            projeto['id'] = str(projeto['_id'])
            projeto.pop('_id')

        projetos = [cls(**projeto) for projeto in projetos]
        return projetos 

    
    @classmethod 
    def update_by_id(cls, data):
        db = init_db()

        projeto = cls.get_by_id(data['id'])
        if not projeto:
            return {"message": "Projeto not found"}, 404
        
        update_data = {k: v for k, v in data.items() if v is not None and k != 'id'}
        result = db.projetos.update_one({'_id': ObjectId(data['id'])}, {
            '$set': update_data
        })

        if result.modified_count == 0:
            return {"message": "No changes made"}, 200

        return {"message": "Projeto updated successfully"}, 200

    @classmethod
    def get_by_processo(cls, processo_id: str):
        db = init_db()
        projetos = list(db.projetos.find({'processo_seletivo': processo_id}))
        if not projetos:
            return None
        for projeto in projetos:
            projeto['id'] = str(projeto['_id'])
            projeto.pop('_id')
        projetos = [cls(**projeto) for projeto in projetos]
        return projetos

    @classmethod
    def update(cls, data):
        db = init_db()

        projeto = cls.get_by_id(data['id'])
        if not projeto:
            return {"message": "Projeto not found"}, 404

        update_data = {k: v for k, v in data.items() if v is not None and k != 'id'}

        response = db.projetos.update_one({'_id': ObjectId(data['id'])}, {
            '$set': update_data
        })

        if response.modified_count == 0:
            return {"message": "No changes were made"}, 400

        return {"message": f"Projeto updated successfully with id {data['id']}"}, 201


    def delete(self):
        db = init_db()
        db.projetos.delete_one({'_id': self.id})

