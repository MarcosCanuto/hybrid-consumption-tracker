from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegistroCreate(BaseModel):
    id_tanque: Optional[int] = None
    id_combustivel: Optional[int] = None
    tipo: str
    data: datetime
    odometro: float
    quantidade: Optional[float] = None
    valor_total: Optional[float] = None
    valor_unitario: Optional[float] = None
    tanque_cheio: Optional[bool] = None
    percentual_tanque: Optional[float] = None
    percentual_bateria: Optional[float] = None
    observacao: Optional[str] = None

class RegistroResponse(BaseModel):
    id: int
    id_veiculo: int
    id_tanque: Optional[int]
    id_combustivel: Optional[int]
    tipo: str
    data: datetime
    odometro: float
    quantidade: Optional[float]
    valor_total: Optional[float]
    valor_unitario: Optional[float]
    tanque_cheio: Optional[bool]
    percentual_tanque: Optional[float]
    percentual_bateria: Optional[float]
    observacao: Optional[str]
    data_criacao: datetime

    model_config = {"from_attributes": True}