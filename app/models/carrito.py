from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Carrito(Base):
    __tablename__ = "carrito"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, index=True)
    items = relationship("ItemsCarrito", back_populates="carrito", cascade="all, delete-orphan")
    cliente = relationship("Usuario", back_populates="carrito")


class ItemsCarrito(Base):
    __tablename__ = "items_carrito"

    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carrito.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, default=1)
    carrito = relationship("Carrito", back_populates="items")
    producto = relationship("Productos", back_populates="itemscarrito")
