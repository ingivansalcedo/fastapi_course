from sqlalchemy import Column, Integer, String, float, boolean, foreignkey
from sqlalchemy.orm import relationship
from app.database import get_db, Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    productos = relationship("Productos", back_populates="categoria")


class Productos(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(float)
    disponible = Column(boolean, default=True)
    categoria_id = Column(Integer, foreignkey("categorias.id"))

    categoria = relationship("Categoria", back_populates="productos")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(boolean, default=True)


