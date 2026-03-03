from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TanqueCombustivel(Base):
    __tablename__ = "tanque_combustivel"

    id = Column(Integer, primary_key=True)
    id_tanque = Column(Integer, ForeignKey("tanque.id"), nullable=False)
    tipo_combustivel = Column(String(50), nullable=False)

    tanque = relationship("Tanque", back_populates="combustiveis")
    registros = relationship("Registro", back_populates="combustivel")