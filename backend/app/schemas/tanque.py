from pydantic import BaseModel
from typing import Optional

class TanqueCreate(BaseModel):
    tipo: str
    unidade: str
    capacidade: Optional[float] = None  

class TanqueResponse(BaseModel):
    id: int
    id_veiculo: int
    tipo: str
    unidade: str
    capacidade: float

    model_config = {"from_attributes": True}