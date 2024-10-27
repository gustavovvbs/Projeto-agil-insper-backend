from pydantic import BaseModel, Field
from models.professor import Professor 
from models.processo_seletivo import ProcessoSeletivo
from models.estudante import Estudante

class Aplicacao(BaseModel):
    pdf_url: str = Field(..., title="URL do PDF", description="URL do PDF da aplicação")
    estudante: Estudante
    professor: Professor
    processo_seletivo: ProcessoSeletivo
    