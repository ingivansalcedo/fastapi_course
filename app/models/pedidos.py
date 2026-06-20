from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


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
