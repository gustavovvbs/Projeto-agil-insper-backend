from pydantic import BaseModel, Field
from database import init_db
from bson import ObjectId

class Professor(BaseModel):
    id: str = Field(None, title="ID", description="ID do professor")
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
        if not professor:
            return None
        professor = db.professores.find_one({'email': professor['email']})
        if not professor:
            return None
        professor['id'] = str(professor['_id'])
        professor.pop('_id')
        return cls(**professor)

    @classmethod
    def get_all(cls):
        db = init_db()
        professores = list(db.professores.find())
        professor_from_users_db = []
        for professor in professores:
            professor_from_users_db.append(db.users.find_one({'email': professor['email']}))
            
        for professor_professor, professor_user in zip(professores, professor_from_users_db):
            professor_professor['id'] = str(professor_user['_id'])
            professor.pop('_id')

        professores = [cls(**professor) for professor in professores]
        return professores