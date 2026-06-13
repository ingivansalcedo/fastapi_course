from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hash_password, verify_password


class DuplicateUserError(Exception):
    """Excepción lanzada cuando se intenta crear un usuario ya existente."""
    pass


class NotFoundError(Exception):
    """Recurso no encontrado."""
    pass


class InvalidDataError(Exception):
    """Datos inválidos o dependencias faltantes (p. ej. categoría no existente)."""
    pass


# ==================== CRUD CATEGORIAS ====================

def get_categoria(db: Session, categoria_id: int):
    """Obtener una categoría por ID"""
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()


def get_categoria_by_nombre(db: Session, nombre: str):
    """Obtener una categoría por nombre"""
    return db.query(models.Categoria).filter(models.Categoria.nombre == nombre).first()


def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todas las categorías con paginación"""
    print ("Obteniendo categorías...")
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Crear una nueva categoría"""
    db_categoria = models.Categoria(nombre=categoria.nombre)
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


# ==================== CRUD PRODUCTOS ====================

def get_producto(db: Session, producto_id: int):
    """Obtener un producto por ID"""
    return db.query(models.Productos).filter(models.Productos.id == producto_id).first()


def get_productos(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todos los productos con paginación"""
    return db.query(models.Productos).offset(skip).limit(limit).all()


def get_productos_by_categoria(db: Session, categoria_id: int, skip: int = 0, limit: int = 100):
    """Obtener productos de una categoría específica"""
    return db.query(models.Productos).filter(
        models.Productos.categoria_id == categoria_id
    ).offset(skip).limit(limit).all()


def get_productos_disponibles(db: Session, skip: int = 0, limit: int = 100):
    """Obtener productos disponibles"""
    return db.query(models.Productos).filter(
        models.Productos.disponible == True
    ).offset(skip).limit(limit).all()


def create_producto(db: Session, producto: schemas.ProductoCreate):
    """Crear un nuevo producto"""
    # Verificar que la categoría existe
    categoria = get_categoria(db, producto.categoria_id)
    if not categoria:
        raise InvalidDataError("Categoría no encontrada")
    
    db_producto = models.Productos(
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

# ==================== CRUD USUARIOS ====================

def get_usuario(db: Session, usuario_id: int):
    """Obtener un usuario por ID"""
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todos los usuarios con paginación"""
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def get_usuario_by_email(db: Session, email: str):
    """Obtener un usuario por email"""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Crear un nuevo usuario"""
    # Verificar si el usuario ya existe por email y evitar duplicados
    existing = get_usuario_by_email(db, usuario.email)
    if existing:
        raise DuplicateUserError("El email ya está registrado")

    db_usuario = models.Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        hashed_password=hash_password(usuario.password),  # En producción, hashea la contraseña
        es_admin=usuario.es_admin,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioUpdate):
    """Actualizar un usuario"""
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        raise NotFoundError("Usuario no encontrado")
    
    if usuario.nombre is not None:
        db_usuario.nombre = usuario.nombre
    if usuario.email is not None:
        db_usuario.email = usuario.email
    if usuario.is_active is not None:
        db_usuario.is_active = usuario.is_active
    if usuario.es_admin is not None:
        db_usuario.es_admin = usuario.es_admin
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    """Eliminar un usuario"""
    db_usuario = get_usuario(db, usuario_id)
    if not db_usuario:
        raise NotFoundError("Usuario no encontrado")

    db.delete(db_usuario)
    db.commit()
    return db_usuario



