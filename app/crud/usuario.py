from sqlalchemy.orm import Session

from app import schemas
from app.core import hash_password
from app.models.usuario import Usuario


class DuplicateUserError(Exception):
    """Excepción lanzada cuando se intenta crear un usuario ya existente."""
    pass


class NotFoundError(Exception):
    """Recurso no encontrado."""
    pass


# ==================== CRUD USUARIOS ====================

def get_usuario(db: Session, usuario_id: int):
    """Obtener un usuario por ID"""
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtener todos los usuarios con paginación"""
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuario_by_email(db: Session, email: str):
    """Obtener un usuario por email"""
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Crear un nuevo usuario"""
    # Verificar si el usuario ya existe por email y evitar duplicados
    existing = get_usuario_by_email(db, usuario.email)
    if existing:
        raise DuplicateUserError("El email ya está registrado")

    db_usuario = Usuario(
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