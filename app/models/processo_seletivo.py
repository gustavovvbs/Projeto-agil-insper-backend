from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from models.projeto import Projeto

class ProcessoSeletivo(BaseModel):
    data_encerramento: date = Field(..., title="Data de Encerramento", description="Data de encerramento do processo seletivo")
    projetos: list[Projeto]