from pydantic import BaseModel, Field 
from database import init_db

class Coordenador(BaseModel):
    nome: str
    email: str  

    def save(self):
        db = init_db()
        db.coordenadores.insert_one({
            'email': self.email,
            'nome': self.nome
        })
