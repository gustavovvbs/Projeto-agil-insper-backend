from pydantic import BaseModel, Field 
from typing import List, Optional
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor 
from bson import ObjectId
from database import init_db

class Projeto(BaseModel):
    id: Optional[str] = None
    processo_seletivo: str = Field(..., title="Processo Seletivo", description="Processo Seletivo's ObjectId")
    titulo: str = Field('Projeto não nomeado', title="Título", description="Título do projeto")
    professor: str = Field(..., title="Professor", description="Professor's ObjectId")
    temas: List[str]
    descricao: str
    aplicacoes: Optional[List[str]] = Field([], title="Aplicações", description="Aplicações do projeto")

    def __init__(self, processo_seletivo: str, professor: str, temas: List[str], descricao: str, aplicacoes: Optional[List[str]] = [], titulo: str = 'Projeto não nomeado', id: Optional[str] = None):
        super().__init__(processo_seletivo=processo_seletivo, professor=professor, temas=temas, descricao=descricao, aplicacoes=aplicacoes, titulo=titulo, id=id)
        self.processo_seletivo = processo_seletivo
        self.professor = professor
        self.temas = temas
        self.descricao = descricao

    def save(self):
        db = init_db()
        self.id = str(db.projetos.insert_one({
            'processo_seletivo': self.processo_seletivo,
            'professor': self.professor,
            'temas': self.temas,
            'descricao': self.descricao
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

    def update(self, data):
        db = init_db()
        
        db.projetos.update_one({'_id': ObjectId(self.id)}, {
            '$set': {
                'processo_seletivo': data['processo_seletivo'],
                'professor': data['professor'],
                'temas': data['temas'],
                'descricao': data['descricao'],
                'aplicacoes': data['aplicacoes']
            }
        })

    def delete(self):
        db = init_db()
        db.projetos.delete_one({'_id': self.id})

