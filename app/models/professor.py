from pydantic import BaseModel, Field
from database import init_db
from bson import ObjectId

class Professor(BaseModel):
    nome: str = Field(..., title="Nome", description="Nome do professor")
    email: str = Field(..., title="Email", description="Email do professor")
    area_pesquisa: str = Field(..., title="Área de Pesquisa", description="Área de pesquisa do professor")
    descricao: str = Field(..., title="Descrição", description="Descrição do professor")
    foto_url: str = Field('', title="URL da Foto", description="URL da foto do professor")


    def save(self):
        db = init_db()
        db.professores.insert_one({
            'email': self.email,
            'nome': self.nome,
            'area_pesquisa': self.area_pesquisa,
            'descricao': self.descricao,
            'foto_url': self.foto_url
        })

    @classmethod
    def get_by_id(cls, id: str):
        db = init_db()
        professor = db.users.find_one({'_id': ObjectId(id)})
        professor = db.professores.find_one({'email': professor['email']})
        if not professor:
            return None
        professor['id'] = str(professor['_id'])
        professor.pop('_id')
        return cls(**professor)