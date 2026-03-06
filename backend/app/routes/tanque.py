from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tanque import Tanque
from app.models.tanque_combustivel import TanqueCombustivel
from app.schemas.tanque import TanqueCreate, TanqueResponse
from app.schemas.tanque_combustivel import TanqueCombustivelCreate, TanqueCombustivelResponse

router = APIRouter(
    prefix="/tanques",
    tags=["Tanques"]
)

@router.post("/", response_model=TanqueResponse)
def criar_tanque(id_veiculo: int, tanque: TanqueCreate, db: Session = Depends(get_db)):
    novo_tanque = Tanque(
        id_veiculo=id_veiculo,
        tipo=tanque.tipo,
        unidade=tanque.unidade,
        capacidade=tanque.capacidade
    )
    db.add(novo_tanque)
    db.commit()
    db.refresh(novo_tanque)
    return novo_tanque

@router.get("/veiculo/{veiculo_id}", response_model=list[TanqueResponse])
def listar_tanques(veiculo_id: int, db: Session = Depends(get_db)):
    tanques = db.query(Tanque).filter(Tanque.id_veiculo == veiculo_id).all()
    return tanques

@router.post("/{tanque_id}/combustiveis", response_model=TanqueCombustivelResponse)
def adicionar_combustivel(tanque_id: int, combustivel: TanqueCombustivelCreate, db: Session = Depends(get_db)):
    tanque = db.query(Tanque).filter(Tanque.id == tanque_id).first()
    if not tanque:
        raise HTTPException(status_code=404, detail="Tanque não encontrado")
    
    novo_combustivel = TanqueCombustivel(
        id_tanque=tanque_id,
        tipo_combustivel=combustivel.tipo_combustivel
    )
    db.add(novo_combustivel)
    db.commit()
    db.refresh(novo_combustivel)
    return novo_combustivel

@router.get("/{tanque_id}/combustiveis", response_model=list[TanqueCombustivelResponse])
def listar_combustiveis(tanque_id: int, db: Session = Depends(get_db)):
    combustiveis = db.query(TanqueCombustivel).filter(TanqueCombustivel.id_tanque == tanque_id).all()
    return combustiveis