from pydantic import BaseModel, Field 
from database import init_db

class Coordenador(BaseModel):
    nome: str
    email: str  

    def __init__(self, nome: str, email: str):
        super().__init__(nome=nome, email=email)
        self.nome = nome
        self.email = email

    def save(self):
        db = init_db()
        db.coordenadores.insert_one({
            'email': self.email,
            'nome': self.nome
        })
