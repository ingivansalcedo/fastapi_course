from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Productos(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    disponible = Column(Boolean, default=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="productos")
    itemscarrito = relationship("ItemsCarrito", back_populates="producto", cascade="all, delete-orphan")
    detalles_pedido = relationship("DetallesPedido", back_populates="producto", cascade="all, delete-orphan")
