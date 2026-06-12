from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.consumos import Consumos
from app.models.registros import Registros
from app.schemas.consumos import ConsumoResponse
from app.auth import get_usuario_atual
from app.models.usuarios import Usuarios


router = APIRouter(
    prefix="/consumos",
    tags=["Consumos"]
)

@router.get("/veiculos/{veiculo_id}", response_model=list[ConsumoResponse])
def listar_consumos(veiculo_id: int, db: Session = Depends(get_db), usuario: Usuarios = Depends(get_usuario_atual)):
    consumos = (
        db.query(Consumos)
        .join(Registros, Consumos.id_registro_origem == Registros.id)
        .filter(Registros.id_veiculo == veiculo_id)
        .order_by(Consumos.id)
        .all()
    )
    return consumos