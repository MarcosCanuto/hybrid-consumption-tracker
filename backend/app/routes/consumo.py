from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumo import Consumo
from app.models.registro import Registro
from app.schemas.consumo import ConsumoResponse

router = APIRouter(
    prefix="/consumos",
    tags=["Consumos"]
)

@router.get("/veiculo/{veiculo_id}", response_model=list[ConsumoResponse])
def listar_consumos(veiculo_id: int, db: Session = Depends(get_db)):
    consumos = (
        db.query(Consumo)
        .join(Registro, Consumo.id_registro_origem == Registro.id)
        .filter(Registro.id_veiculo == veiculo_id)
        .order_by(Consumo.id)
        .all()
    )
    return consumos