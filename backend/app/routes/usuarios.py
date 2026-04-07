from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuarios
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuarios).filter(Usuarios.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    novo_usuario = Usuarios(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha,
        unidade_consumo_eletrico=usuario.unidade_consumo_eletrico,
        unidade_consumo_combustivel=usuario.unidade_consumo_combustivel
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario