from sqlalchemy.orm import Session

from app.models.carrito import Carrito
from app.models.pedidos import DetallesPedido, Pedidos
from app.models.producto import Productos


def get_pedidos(db: Session, cliente_id: int):
    """Obtener todos los pedidos de un cliente."""
    return db.query(Pedidos).filter(Pedidos.usuario_id == cliente_id).all()

def crear_pedido(db: Session, cliente_id: int):
    """Crear un pedido a partir del carrito de un cliente."""
    carrito = db.query(Carrito).filter(Carrito.cliente_id == cliente_id).first()
    if not carrito or not carrito.items:
        raise ValueError("El carrito está vacío o no existe")

    pedido = Pedidos(usuario_id=cliente_id, total=0)
    db.add(pedido)
    db.flush()  # Para obtener el ID del pedido antes de agregar los items

    total_pedido = 0.0

    for item in carrito.items:
        producto = db.query(Productos).filter(Productos.id == item.producto_id).first()
        if not producto:
            raise ValueError(f"Producto {item.producto_id} no encontrado")
        if item.cantidad <= 0:
            raise ValueError(f"Cantidad inválida para el producto {item.producto_id}")
        if not producto.disponible or producto.stock <= 0:
            raise ValueError(f"El producto '{producto.nombre}' no está disponible o no tiene stock")
        if producto.precio < 0:
            raise ValueError(f"El producto '{producto.nombre}' tiene un precio inválido")
        if item.cantidad > producto.stock:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {item.cantidad}"
            )

        precio = producto.precio
        item_pedido = DetallesPedido(
            pedido_id=pedido.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            precio_unitario=precio,
        )
        db.add(item_pedido)

        producto.stock -= item.cantidad
        if producto.stock == 0:
            producto.disponible = False

        total_pedido += precio * item.cantidad

    pedido.total = total_pedido

    # Vaciar el carrito después de crear el pedido
    for item in carrito.items:
        db.delete(item)

    db.commit()
    db.refresh(pedido)
    return pedido

def get_pedido(db: Session, pedido_id: int, cliente_id: int):
    """Obtener un pedido específico de un cliente."""
    return db.query(Pedidos).filter(Pedidos.id == pedido_id, Pedidos.usuario_id == cliente_id).first()
