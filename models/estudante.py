from pydantic import BaseModel, Field
from typing import List, Optional
from database import init_db
from bson import ObjectId

class Estudante(BaseModel):

    id: Optional[str] = None
    nome: str = Field(..., title="Nome", description="Nome do estudante")
    email: str = Field(..., title="Email", description="Email do estudante")
    curso: str = Field(..., title="Curso", description="Curso do estudante")
    semestre: str = Field(..., title="Semestre", description="Semestre do estudante")

    def save(self):
        """ 
        Saves the student instance to the database. 

        Inserts a new document into the 'estudantes' collection with the student's details.
        """
        db = init_db()
        db.estudantes.insert_one({
            'email': self.email,
            'nome': self.nome,
            'curso': self.curso,
            'semestre': self.semestre
        })

    @classmethod
    def get_by_id(cls, id):
        """ 
        Retrieves a student by their user's db ID. 

        Queries the 'users' collection for a user with the given ID, then queries the 'estudantes' collection for a student with the same email.

        Args:
            id (str): The ID of the user to retrieve.

        Returns:
            Estudante: The student with the given ID.
        """
        db = init_db()
        estudante = db.users.find_one({'_id': ObjectId(id)})
        if not estudante:
            return None
        estudante_from_estudantes_db = db.estudantes.find_one({'email': estudante['email']})
        if not estudante_from_estudantes_db:
            print("FUDEU CONFLITO GRAVISSIMO CASCATA N APAGOU NOS DOIS DB CONSERTA AGR SE N FODEU **********************************************************************************************************************")
            return None
        estudante_from_estudantes_db['id'] = str(estudante['_id'])
        estudante_from_estudantes_db.pop('_id')
        return cls(**estudante_from_estudantes_db)

    