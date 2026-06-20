from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
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

class Pedidos(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    fecha_pedido = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="pedidos")
    detalles = relationship("DetallesPedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallesPedido(Base):
    __tablename__ = "detalles_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
    pedido = relationship("Pedidos", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_pedido")
