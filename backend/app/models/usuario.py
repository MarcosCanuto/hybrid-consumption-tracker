from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    unidade_consumo_eletrico = Column(String(20), nullable=False, default="km_kwh")
    unidade_consumo_combustivel = Column(String(20), nullable=False, default="km_l")
    data_criacao = Column(DateTime, nullable=False, server_default=func.now())

    veiculos = relationship("Veiculo", back_populates="usuario")