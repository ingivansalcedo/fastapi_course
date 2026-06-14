from sqlalchemy.orm import Session

from app import schemas
from app.crud.categoria import get_categoria
from app.models.producto import Productos


class NotFoundError(Exception):
    """Recurso no encontrado."""
    pass


class InvalidDataError(Exception):
    """Datos inválidos o dependencias faltantes (p. ej. categoría no existente)."""
    pass

# ==================== CRUD PRODUCTOS ====================

def get_producto(db: Session, producto_id: int):
    """Obtener un producto por ID"""
    return db.query(Productos).filter(Productos.id == producto_id).first()


def get_productos(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todos los productos con paginación"""
    return db.query(Productos).offset(skip).limit(limit).all()


def get_productos_by_categoria(db: Session, categoria_id: int, skip: int = 0, limit: int = 100):
    """Obtener productos de una categoría específica"""
    return db.query(Productos).filter(
        Productos.categoria_id == categoria_id
    ).offset(skip).limit(limit).all()


def get_productos_disponibles(db: Session, skip: int = 0, limit: int = 100):
    """Obtener productos disponibles"""
    return db.query(Productos).filter(Productos.disponible).offset(skip).limit(limit).all()


def create_producto(db: Session, producto: schemas.ProductoCreate):
    """Crear un nuevo producto"""
    # Verificar que la categoría existe
    categoria = get_categoria(db, producto.categoria_id)
    if not categoria:
        raise InvalidDataError("Categoría no encontrada")
    
    db_producto = Productos(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        disponible=producto.disponible,
        categoria_id=producto.categoria_id
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    """Actualizar un producto"""
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        raise NotFoundError("Producto no encontrado")
    
    # Validar categoría si se intenta cambiar
    if producto.categoria_id is not None:
        categoria = get_categoria(db, producto.categoria_id)
        if not categoria:
            raise InvalidDataError("Categoría inválida")
    
    if producto.nombre is not None:
        db_producto.nombre = producto.nombre
    if producto.descripcion is not None:
        db_producto.descripcion = producto.descripcion
    if producto.precio is not None:
        db_producto.precio = producto.precio
    if producto.disponible is not None:
        db_producto.disponible = producto.disponible
    if producto.categoria_id is not None:
        db_producto.categoria_id = producto.categoria_id
    
    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, producto_id: int):
    """Eliminar un producto"""
    db_producto = get_producto(db, producto_id)
    if not db_producto:
        raise NotFoundError("Producto no encontrado")

    db.delete(db_producto)
    db.commit()
    return db_producto
