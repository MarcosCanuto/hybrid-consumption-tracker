from sqlalchemy import BigInteger, Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    unidade_consumo_eletrico = Column(String(20), nullable=False, default="km_kwh")
    unidade_consumo_combustivel = Column(String(20), nullable=False, default="km_l")
    data_criacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    veiculos = relationship("Veiculos", back_populates="usuarios")