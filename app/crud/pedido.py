from sqlalchemy.orm import Session

from app.models.pedidos import Carrito, DetallesPedido, Pedidos
from app.models.producto import Productos


def get_pedidos(db: Session, cliente_id: int):
    """Obtener todos los pedidos de un cliente."""
    return db.query(Pedidos).filter(Pedidos.usuario_id == cliente_id).all()

def crear_pedido(db: Session, cliente_id: int):
    """Crear un pedido a partir del carrito de un cliente."""
    carrito = db.query(Carrito).filter(Carrito.cliente_id == cliente_id).first()
    if not carrito or not carrito.items:
        raise ValueError("El carrito está vacío o no existe")

    pedido = Pedidos(usuario_id=cliente_id)
    db.add(pedido)
    db.flush()  # Para obtener el ID del pedido antes de agregar los items

    for item in carrito.items:
        producto = db.query(Productos).filter(Productos.id == item.producto_id).first()
        precio = producto.precio if producto else 0.0
        item_pedido = DetallesPedido(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=precio,
        )
        db.add(item_pedido)

    # Vaciar el carrito después de crear el pedido
    for item in carrito.items:
        db.delete(item)

    db.commit()
    db.refresh(pedido)
    return pedido

def get_pedido(db: Session, pedido_id: int, cliente_id: int):
    """Obtener un pedido específico de un cliente."""
    return db.query(Pedidos).filter(Pedidos.id == pedido_id, Pedidos.usuario_id == cliente_id).first()
