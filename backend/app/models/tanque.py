from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tanque(Base):
    __tablename__ = "tanque"

    id = Column(Integer, primary_key=True)
    id_veiculo = Column(Integer, ForeignKey("veiculo.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    unidade = Column(String(20), nullable=False)
    capacidade = Column(Numeric(8, 2))

    veiculo = relationship("Veiculo", back_populates="tanques")
    combustiveis = relationship("TanqueCombustivel", back_populates="tanque")
    registros = relationship("Registro", back_populates="tanque")