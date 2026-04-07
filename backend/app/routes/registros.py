from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.registros import Registros
from app.schemas.registros import RegistroCreate, RegistroResponse
from app.services.calculo_consumo import calcular_consumo

router = APIRouter(
    prefix="/registros",
    tags=["Registros"]
)

@router.post("/", response_model=RegistroResponse)
def criar_registro(id_veiculo: int, registro: RegistroCreate, db: Session = Depends(get_db)):
    if registro.tipo == "abastecimento" and registro.id_tanque is None:
        raise HTTPException(status_code=400, detail="Abastecimento requer id_tanque")
    
    if registro.tipo == "abastecimento" and registro.quantidade is None:
        raise HTTPException(status_code=400, detail="Abastecimento requer quantidade")

    novo_registro = Registros(
        id_veiculo=id_veiculo,
        id_tanque=registro.id_tanque,
        id_combustivel=registro.id_combustivel,
        tipo=registro.tipo,
        data=registro.data,
        odometro=registro.odometro,
        quantidade=registro.quantidade,
        valor_total=registro.valor_total,
        valor_unitario=registro.valor_unitario,
        tanque_cheio=registro.tanque_cheio,
        percentual_tanque=registro.percentual_tanque,
        percentual_bateria=registro.percentual_bateria,
        observacao=registro.observacao
    )
    db.add(novo_registro)
    db.commit()
    db.refresh(novo_registro)
    calcular_consumo(db, novo_registro)  # Calcula consumo após criar o registro
    return novo_registro

@router.get("/veiculos/{veiculo_id}", response_model=list[RegistroResponse])
def listar_registros(veiculo_id: int, db: Session = Depends(get_db)):
    registros = db.query(Registros).filter(
        Registros.id_veiculo == veiculo_id
    ).order_by(Registros.data).all()
    return registros

@router.get("/{registro_id}", response_model=RegistroResponse)
def buscar_registro(registro_id: int, db: Session = Depends(get_db)):
    registro = db.query(Registros).filter(Registros.id == registro_id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return registro

@router.put("/{registro_id}", response_model=RegistroResponse)
def atualizar_registro(registro_id: int, registro: RegistroCreate, db: Session = Depends(get_db)):
    db_registro = db.query(Registros).filter(Registros.id == registro_id).first()
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    for campo, valor in registro.model_dump(exclude_unset=True).items():
        setattr(db_registro, campo, valor)
    
    db.commit()
    db.refresh(db_registro)
    return db_registro