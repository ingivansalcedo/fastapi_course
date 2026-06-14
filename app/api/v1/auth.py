from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core import security
from app.db.database import get_db
from app.deps import get_current_user, requires_admin

api_router = APIRouter()



# ==================== ENDPOINTS USUARIOS ====================



@api_router.get("/usuarios", response_model=list[schemas.UsuarioResponse], )
def listar_usuarios(db: Session = Depends(get_db)):
    print("Obteniendo usuarios...")
    return crud.get_usuarios(db)

@api_router.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@api_router.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):

    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    
    try:
        return crud.create_usuario(db, usuario)
    except crud.DuplicateUserError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@api_router.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    try:
        crud.delete_usuario(db, usuario_id)
        return {"mensaje": "Usuario eliminado"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Intentando login para email: {form_data.username}")
    """
    Endpoint de login: valida email y contraseña, devuelve token JWT.

    Args:
        form_data: Datos enviados por OAuth2 password flow (username + password).
        db: Sesión de base de datos.

    Returns:
        Token JWT con tipo "bearer".
    
    Raises:
        HTTPException: 401 si las credenciales son inválidas.
    """
    user = crud.get_usuario_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.get("/me", response_model=schemas.UsuarioResponse)
def leer_usuario_actual(current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    """
    Endpoint para obtener información del usuario autenticado.

    Args:
        current_user: Usuario autenticado obtenido de la dependencia get_current_user.
    Returns:
        Información del usuario actual. Si el token es inválido o el usuario no existe, se lanza una excepción HTTP 401.
    """
    return current_user

@api_router.get("/admin/ping")
def admin_ping(current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    """
    Endpoint de prueba para administradores.

    Args:
        current_user: Usuario autenticado obtenido de la dependencia get_current_user.
    Returns:
        Un mensaje de ping si el usuario es administrador. Si el usuario no es administrador, se lanza una excepción HTTP 403.
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    return {"message": "Pong! Solo los administradores pueden ver esto."}

