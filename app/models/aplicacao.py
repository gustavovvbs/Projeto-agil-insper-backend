from pydantic import BaseModel, Field
from models.professor import Professor 
from typing import List, Optional
from models.processo_seletivo import ProcessoSeletivo
from models.estudante import Estudante
from database import init_db

class Aplicacao(BaseModel):
    id: Optional[str] = None
    pdf_url: str = Field(None, title="URL do PDF", description="URL do PDF da aplicação")
    estudante: str = Field(..., title="Estudante", description="Estudante's ObjectId")
    projeto: str = Field(..., title="Projeto", description="Projeto's ObjectId")
    processo_seletivo: str = Field(..., title="Processo Seletivo", description="Processo Seletivo's ObjectId")
    estudante_lattes: str = Field(None, title="Estudante Lattes", description="Estudante's Lattes URL")
    
    def __init__(self, pdf_url: str, estudante: Estudante, projeto: str, processo_seletivo: str, estudante_lattes: str = None, id: Optional[str] = None):
        super().__init__(pdf_url=pdf_url, estudante=estudante, projeto=projeto, processo_seletivo=processo_seletivo, estudante_lattes=estudante_lattes, id=id)
     

    def save(self):
        db = init_db()
        self.id = str(db.aplicacoes.insert_one({
            'pdf_url': self.pdf_url,
            'estudante': self.estudante,
            'projeto': self.projeto,
            'processo_seletivo': self.processo_seletivo,
            'estudante_lattes': self.estudante_lattes
        }).inserted_id)
        

    @classmethod
    def get_by_id(cls, id: str):
        db = init_db()
        aplicacao = db.aplicacoes.find_one({'_id': ObjectId(id)})
        aplicacao['id'] = str(aplicacao['_id'])
        aplicacao.pop('_id')
        return cls(**aplicacao) if aplicacao else None

    @classmethod
    def get_all(cls):
        db = init_db()
        aplicacoes = list(db.aplicacoes.find())
        for aplicacao in aplicacoes:
            aplicacao['id'] = str(aplicacao['_id'])
            aplicacao.pop('_id')

        aplicacoes = [cls(**aplicacao) for aplicacao in aplicacoes]
        return aplicacoes

    @staticmethod
    def update(data):
        db = init_db()
        db.aplicacoes.update_one({'_id': data.id}, {
            '$set': {
                'pdf_url': data['pdf_url'],
                'estudante': data['estudante'],
                'projeto': data['projeto'],
                'processo_seletivo': data['processo_seletivo']
            }
        })
