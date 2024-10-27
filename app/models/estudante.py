from pydantic import BaseModel, Field
from typing import List, Optional
from database import init_db

class Estudante(BaseModel):
    nome: str = Field(..., title="Nome", description="Nome do estudante")
    email: str = Field(..., title="Email", description="Email do estudante")
    curso: str = Field(..., title="Curso", description="Curso do estudante")
    semestre: str = Field(..., title="Semestre", description="Semestre do estudante")

    def __init__(self, nome: str, email: str, curso: str, semestre: int):
        super().__init__(nome=nome, email=email, curso=curso, semestre=semestre)
        self.nome = nome
        self.email = email
        self.curso = curso
        self.semestre = semestre

    def save(self):
        db = init_db()
        db.estudantes.insert_one({
            'email': self.email,
            'nome': self.nome,
            'curso': self.curso,
            'semestre': self.semestre
        })


    