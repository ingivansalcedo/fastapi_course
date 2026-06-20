from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_current_user, get_db

api_router = APIRouter()

@api_router.get("/carrito", response_model=schemas.CarritoResponse)
def obtener_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    return crud.get_carrito(db, current_user.id)

@api_router.post("/carrito/items", response_model=schemas.CarritoResponse)
def agregar_item_al_carrito(item: schemas.ItemCarritoCreate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.agregar_item_al_carrito(db, current_user.id, item.producto_id, item.cantidad)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/carrito/items/{producto_id}", response_model=schemas.CarritoResponse)
def eliminar_item_del_carrito(producto_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.eliminar_item_del_carrito(db, current_user.id, producto_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/carrito/vaciar", response_model=schemas.CarritoResponse)
def vaciar_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.vaciar_carrito(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/carrito", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        crud.eliminar_carrito(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
