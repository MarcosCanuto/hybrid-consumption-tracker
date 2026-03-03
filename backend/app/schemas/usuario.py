from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    unidade_consumo_eletrico: Optional[str] = "km_kwh"
    unidade_consumo_combustivel: Optional[str] = "km_l"

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    unidade_consumo_eletrico: str
    unidade_consumo_combustivel: str
    data_criacao: datetime

    model_config = {"from_attributes": True}