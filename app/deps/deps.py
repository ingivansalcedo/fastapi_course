from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm.session import Session

from app import crud
from app.core.security import verify_token
from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependencia para obtener el usuario actual a partir del token JWT.

    Args:
        token: El token JWT proporcionado en la solicitud.
        db: Sesión de base de datos.
    Returns:
        El usuario autenticado. Si el token no es válido o el usuario no existe, se lanza una excepción HTTP 401.
    """
    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = crud.get_usuario_by_email(db, email=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def requires_admin(user = Depends(get_current_user)):
    """
    Dependencia para verificar que el usuario actual tiene permisos de administrador.

    Args:
        user: El usuario autenticado obtenido de get_current_user.
    Returns:
        El usuario si es administrador. Si no es administrador, se lanza una excepción HTTP 403.
    """
    if not user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    return user

"""Utilidades para manejo de contraseñas usando bcrypt a través de PassLib. Incluye funciones para hashear y verificar contraseñas, 
con configuración ajustable del coste de bcrypt vía variable de entorno.
"""