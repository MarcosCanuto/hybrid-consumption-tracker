from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumos import Consumos
from app.models.registros import Registros
from app.schemas.consumos import ConsumoResponse

router = APIRouter(
    prefix="/consumos",
    tags=["Consumos"]
)

@router.get("/veiculos/{veiculo_id}", response_model=list[ConsumoResponse])
def listar_consumos(veiculo_id: int, db: Session = Depends(get_db)):
    consumos = (
        db.query(Consumos)
        .join(Registros, Consumos.id_registro_origem == Registros.id)
        .filter(Registros.id_veiculo == veiculo_id)
        .order_by(Consumos.id)
        .all()
    )
    return consumos