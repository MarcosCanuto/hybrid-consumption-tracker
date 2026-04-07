from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TanquesCombustivel(Base):
    __tablename__ = "tanques_combustivel"

    id = Column(Integer, primary_key=True)
    id_tanque = Column(Integer, ForeignKey("tanques.id"), nullable=False)
    tipo_combustivel = Column(String(50), nullable=False)

    tanques = relationship("Tanques", back_populates="combustiveis")
    registros = relationship("Registros", back_populates="combustiveis")