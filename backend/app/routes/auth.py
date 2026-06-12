from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import verificar_senha, criar_token
from app.models.usuarios import Usuarios
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuarios).filter(Usuarios.email == form.username).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    token = criar_token({"sub": str(usuario.id)})
    return {"access_token": token, "token_type": "bearer"}
