from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_db, requires_admin

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
