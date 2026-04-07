from pydantic import BaseModel

class TanqueCombustivelCreate(BaseModel):
    tipo_combustivel: str

class TanqueCombustivelResponse(BaseModel):
    id: int
    id_tanque: int
    tipo_combustivel: str

    model_config = {"from_attributes": True}