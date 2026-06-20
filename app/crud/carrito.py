from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.pedidos import Carrito


def crear_carrito(db: Session, cliente_id: int):
    """Crear un carrito para un cliente."""
    carrito = Carrito(cliente_id=cliente_id)
    db.add(carrito)
    try:
        db.commit()
    except IntegrityError:
        # Evita error por carrera cuando dos requests intentan crear el mismo carrito.
        db.rollback()
        carrito = db.query(Carrito).filter(Carrito.cliente_id == cliente_id).first()
        if carrito:
            return carrito
        raise
    db.refresh(carrito)
    return carrito


def get_carrito(db: Session, cliente_id: int, crear_si_no_existe: bool = True):
    """Obtener el carrito de un cliente por su ID.

    Si `crear_si_no_existe` es True y no existe carrito, se crea uno nuevo.
    """
    carrito = db.query(Carrito).filter(Carrito.cliente_id == cliente_id).first()
    if not carrito and crear_si_no_existe:
        carrito = crear_carrito(db, cliente_id)

    return carrito



def agregar_item_al_carrito(db: Session, cliente_id: int, producto_id: int, cantidad: int):
    """Agregar un producto al carrito de un cliente."""
    carrito = get_carrito(db, cliente_id)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    item = next((item for item in carrito.items if item.producto_id == producto_id), None)
    if item:
        item.cantidad += cantidad
    else:
        from app.models.pedidos import ItemsCarrito
        nuevo_item = ItemsCarrito(carrito_id=carrito.id, producto_id=producto_id, cantidad=cantidad)
        db.add(nuevo_item)

    db.commit()
    db.refresh(carrito)
    return carrito


def eliminar_item_del_carrito(db: Session, cliente_id: int, producto_id: int):
    """Eliminar un producto del carrito de un cliente."""
    carrito = get_carrito(db, cliente_id, crear_si_no_existe=False)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    item = next((item for item in carrito.items if item.producto_id == producto_id), None)
    if item:
        db.delete(item)
        db.commit()
        db.refresh(carrito)

    return carrito


def vaciar_carrito(db: Session, cliente_id: int):
    """Vaciar el carrito de un cliente."""
    carrito = get_carrito(db, cliente_id, crear_si_no_existe=False)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    for item in carrito.items:
        db.delete(item)

    db.commit()
    db.refresh(carrito)
    return carrito

def eliminar_carrito(db: Session, cliente_id: int):
    """Eliminar el carrito de un cliente."""
    carrito = get_carrito(db, cliente_id, crear_si_no_existe=False)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    db.delete(carrito)
    db.commit()
