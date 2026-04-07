from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Registros(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True)
    id_veiculo = Column(Integer, ForeignKey("veiculos.id"), nullable=False)
    id_tanque = Column(Integer, ForeignKey("tanques.id"))
    id_combustivel = Column(Integer, ForeignKey("tanques_combustivel.id"))
    tipo = Column(String(20), nullable=False)
    data = Column(DateTime, nullable=False)
    odometro = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Numeric(8, 3))
    valor_total = Column(Numeric(10, 2))
    valor_unitario = Column(Numeric(10, 4))
    tanque_cheio = Column(Boolean)
    percentual_tanque = Column(Numeric(5, 2))
    percentual_bateria = Column(Numeric(5, 2))
    observacao = Column(Text)
    data_criacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    veiculos = relationship("Veiculos", back_populates="registros")
    tanques = relationship("Tanques", back_populates="registros")
    combustiveis = relationship("TanquesCombustivel", back_populates="registros")
    consumos_origem = relationship("Consumos", foreign_keys="Consumos.id_registro_origem", back_populates="registro_origem")
    consumos_destino = relationship("Consumos", foreign_keys="Consumos.id_registro_destino", back_populates="registro_destino")