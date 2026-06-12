from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuarios import Usuarios
from app.schemas.usuarios import UsuarioCreate, UsuarioResponse
from app.auth import hash_senha, verificar_senha, criar_token, get_usuario_atual

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

@router.get("/me", response_model=UsuarioResponse)
def meu_perfil(usuario_atual: Usuarios = Depends(get_usuario_atual)):
    if not usuario_atual:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_atual