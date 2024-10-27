from pydantic import BaseModel, Field 
from models.processo_seletivo import ProcessoSeletivo
from models.professor import Professor 

class Projeto(BaseModel):
    processo_seletivo: ProcessoSeletivo
    professor: Professor 
    temas: list[str]
    descricao: str 