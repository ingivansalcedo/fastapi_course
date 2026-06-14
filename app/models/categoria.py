from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    productos = relationship("Productos", back_populates="categoria")
