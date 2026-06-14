
from sqlalchemy.orm import Session

from app import schemas
from app.models.categoria import Categoria


class NotFoundError(Exception):
    """Recurso no encontrado."""
    pass

# ==================== CRUD CATEGORIAS ====================

def get_categoria(db: Session, categoria_id: int):
    """Obtener una categoría por ID"""
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def get_categoria_by_nombre(db: Session, nombre: str):
    """Obtener una categoría por nombre"""
    return db.query(Categoria).filter(Categoria.nombre == nombre).first()


def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todas las categorías con paginación"""
    print ("Obteniendo categorías...")
    return db.query(Categoria).offset(skip).limit(limit).all()


def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Crear una nueva categoría"""
    db_categoria = Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaUpdate):
    """Actualizar una categoría"""
    db_categoria = get_categoria(db, categoria_id)
    if not db_categoria:
        raise NotFoundError("Categoría no encontrada")

    if categoria.nombre is not None:
        db_categoria.nombre = categoria.nombre

    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def delete_categoria(db: Session, categoria_id: int):
    """Eliminar una categoría"""
    db_categoria = get_categoria(db, categoria_id)
    if not db_categoria:
        raise NotFoundError("Categoría no encontrada")

    db.delete(db_categoria)
    db.commit()
    return db_categoria
