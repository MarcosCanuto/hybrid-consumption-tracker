from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VeiculoCreate(BaseModel):
    apelido: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None

class VeiculoResponse(BaseModel):
    id: int
    id_usuario: int
    apelido: str
    marca: Optional[str]
    modelo: Optional[str]
    ano: Optional[int]
    data_criacao: datetime

    model_config = {"from_attributes": True}