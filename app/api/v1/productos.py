from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.database import get_db
from app.deps import requires_admin

api_router = APIRouter()


# ==================== ENDPOINTS PRODUCTOS ====================


@api_router.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.get_productos(db)


@api_router.post("/productos", response_model=schemas.ProductoResponse)
def agregar_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):

    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )

    try:
        return crud.create_producto(db, producto)
    except crud.InvalidDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )

    try:
        return crud.update_producto(db, producto_id, producto)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except crud.InvalidDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    try:
        crud.delete_producto(db, producto_id)
        return {"mensaje": "Producto eliminado"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
