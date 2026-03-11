from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConsumoResponse(BaseModel):
    id: int
    id_registro_origem: int
    id_registro_destino: int
    tipo: str
    km_percorridos: float
    consumo_eletrico: Optional[float]
    consumo_combustao: Optional[float]
    nivel_confianca: float
    data_calculo: datetime

    model_config = {"from_attributes": True}