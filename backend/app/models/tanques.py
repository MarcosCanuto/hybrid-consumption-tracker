from sqlalchemy import BigInteger, Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Tanques(Base):
    __tablename__ = "tanques"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_veiculo = Column(BigInteger, ForeignKey("veiculos.id"), nullable=False)
    tipo = Column(String(20), nullable=False)
    unidade = Column(String(20), nullable=False)
    capacidade = Column(Numeric(8, 2))

    veiculos = relationship("Veiculos", back_populates="tanques")
    combustiveis = relationship("TanquesCombustivel", back_populates="tanques")
    registros = relationship("Registros", back_populates="tanques")