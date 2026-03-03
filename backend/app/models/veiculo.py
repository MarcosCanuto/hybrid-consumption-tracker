from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Veiculo(Base):
    __tablename__ = "veiculo"

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    apelido = Column(String(100), nullable=False)
    marca = Column(String(100))
    modelo = Column(String(100))
    ano = Column(Integer)
    data_criacao = Column(DateTime, nullable=False, server_default=func.now())

    usuario = relationship("Usuario", back_populates="veiculos")
    tanques = relationship("Tanque", back_populates="veiculo")
    registros = relationship("Registro", back_populates="veiculo")