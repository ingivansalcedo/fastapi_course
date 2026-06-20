from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.carrito import Carrito, ItemsCarrito
from app.models.producto import Productos


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
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0")

    producto = db.query(Productos).filter(Productos.id == producto_id).first()
    if not producto:
        raise ValueError("Producto no encontrado")
    if not producto.disponible:
        raise ValueError("El producto no está disponible")
    if producto.stock <= 0:
        raise ValueError("El producto no tiene stock disponible")

    carrito = get_carrito(db, cliente_id)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    item = next((item for item in carrito.items if item.producto_id == producto_id), None)
    cantidad_en_carrito = item.cantidad if item else 0
    cantidad_total = cantidad_en_carrito + cantidad
    if cantidad_total > producto.stock:
        raise ValueError(
            f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, en carrito: {cantidad_en_carrito}, solicitado adicional: {cantidad}"
        )

    if item:
        item.cantidad = cantidad_total
    else:
        nuevo_item = ItemsCarrito(carrito_id=carrito.id, producto_id=producto_id, cantidad=cantidad)
        db.add(nuevo_item)

    db.commit()
    db.refresh(carrito)
    return carrito


def actualizar_cantidad_item_carrito(db: Session, cliente_id: int, producto_id: int, cantidad: int):
    """Actualizar la cantidad de un producto existente en el carrito."""
    if cantidad < 0:
        raise ValueError("La cantidad no puede ser menor a 0")

    carrito = get_carrito(db, cliente_id, crear_si_no_existe=False)
    if not carrito:
        raise ValueError("Carrito no encontrado para el cliente")

    item = next((item for item in carrito.items if item.producto_id == producto_id), None)
    if not item:
        raise ValueError("El producto no existe en el carrito")

    if cantidad == 0:
        db.delete(item)
        db.commit()
        db.refresh(carrito)
        return carrito

    producto = db.query(Productos).filter(Productos.id == producto_id).first()
    if not producto:
        raise ValueError("Producto no encontrado")
    if not producto.disponible:
        raise ValueError("El producto no está disponible")
    if producto.stock <= 0:
        raise ValueError("El producto no tiene stock disponible")
    if cantidad > producto.stock:
        raise ValueError(
            f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, solicitado: {cantidad}"
        )

    item.cantidad = cantidad
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
