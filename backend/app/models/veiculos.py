from sqlalchemy import BigInteger, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Veiculos(Base):
    __tablename__ = "veiculos"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_usuario = Column(BigInteger, ForeignKey("usuarios.id"), nullable=False, autoincrement=True)
    apelido = Column(String(100), nullable=False)
    marca = Column(String(100))
    modelo = Column(String(100))
    ano = Column(Integer)
    data_criacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    usuarios = relationship("Usuarios", back_populates="veiculos")
    tanques = relationship("Tanques", back_populates="veiculos")
    registros = relationship("Registros", back_populates="veiculos")