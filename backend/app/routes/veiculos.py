from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.veiculos import Veiculos
from app.schemas.veiculos import VeiculoCreate, VeiculoResponse

router = APIRouter(
    prefix="/veiculos",
    tags=["Veículos"]
)

@router.post("/", response_model=VeiculoResponse)
def criar_veiculo(id_usuario: int, veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    novo_veiculo = Veiculos(
        id_usuario=id_usuario,
        apelido=veiculo.apelido,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        ano=veiculo.ano
    )
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    return novo_veiculo

@router.get("/{veiculo_id}", response_model=VeiculoResponse)
def buscar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    veiculo = db.query(Veiculos).filter(Veiculos.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

@router.get("/usuario/{usuario_id}", response_model=list[VeiculoResponse])
def listar_veiculos(usuario_id: int, db: Session = Depends(get_db)):
    veiculos = db.query(Veiculos).filter(Veiculos.id_usuario == usuario_id).all()
    return veiculos