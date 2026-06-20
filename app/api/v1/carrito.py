from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_current_user, get_db

api_router = APIRouter()

@api_router.get("/carrito", response_model=schemas.CarritoResponse,
                summary="Obtener carrito", description="Obtener los detalles del carrito del usuario actual",
                response_description="Detalles del carrito")
def obtener_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    return crud.get_carrito(db, current_user.id)

@api_router.post("/carrito/items", response_model=schemas.CarritoResponse,
                 summary="Agregar item al carrito", description="Agregar un nuevo item al carrito del usuario actual",
                 response_description="Item agregado al carrito exitosamente")
def agregar_item_al_carrito(item: schemas.ItemCarritoCreate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.agregar_item_al_carrito(db, current_user.id, item.producto_id, item.cantidad)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.put("/carrito/items/{producto_id}", response_model=schemas.CarritoResponse,
                summary="Actualizar cantidad de item en el carrito", description="Actualizar la cantidad de un item específico en el carrito del usuario actual",
                response_description="Cantidad de item actualizada exitosamente")
def actualizar_cantidad_item_carrito(producto_id: int, item: schemas.ItemCarritoUpdate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.actualizar_cantidad_item_carrito(db, current_user.id, producto_id, item.cantidad)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@api_router.delete("/carrito/items/{producto_id}", response_model=schemas.CarritoResponse,
                   summary="Eliminar item del carrito", description="Eliminar un item específico del carrito del usuario actual",
                   response_description="Item eliminado del carrito exitosamente")
def eliminar_item_del_carrito(producto_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.eliminar_item_del_carrito(db, current_user.id, producto_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/carrito/vaciar", response_model=schemas.CarritoResponse,
                   summary="Vaciar carrito", description="Eliminar todos los items del carrito del usuario actual",
                   response_description="Carrito vaciado exitosamente")
def vaciar_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.vaciar_carrito(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@api_router.delete("/carrito", status_code=status.HTTP_204_NO_CONTENT,
                   summary="Eliminar carrito", description="Eliminar el carrito del usuario actual",
                   response_description="Carrito eliminado exitosamente")
def eliminar_carrito(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        crud.eliminar_carrito(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
