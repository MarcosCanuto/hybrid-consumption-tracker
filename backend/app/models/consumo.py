from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Consumo(Base):
    __tablename__ = "consumo"

    id = Column(Integer, primary_key=True)
    id_registro_origem = Column(Integer, ForeignKey("registro.id"), nullable=False)
    id_registro_destino = Column(Integer, ForeignKey("registro.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    km_percorridos = Column(Numeric(10, 2), nullable=False)
    consumo_eletrico = Column(Numeric(8, 4))
    consumo_combustao = Column(Numeric(8, 4))
    nivel_confianca = Column(Numeric(5, 2), nullable=False)
    data_calculo = Column(DateTime, nullable=False, server_default=func.now())

    registro_origem = relationship("Registro", foreign_keys=[id_registro_origem], back_populates="consumos_origem")
    registro_destino = relationship("Registro", foreign_keys=[id_registro_destino], back_populates="consumos_destino")