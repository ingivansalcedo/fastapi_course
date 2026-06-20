from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_current_user, get_db

api_router = APIRouter()

@api_router.get("/pedidos", response_model=list[schemas.PedidoResponse],
                summary="Listar pedidos", description="Obtener la lista de pedidos del usuario actual",
                response_description="Lista de pedidos")
def obtener_pedidos(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    return crud.get_pedidos(db, current_user.id)

@api_router.post("/pedidos", response_model=schemas.PedidoResponse, status_code=status.HTTP_201_CREATED,
                 summary="Crear pedido", description="Crear un nuevo pedido",
                 response_description="Pedido creado exitosamente")
def crear_pedido(db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    try:
        return crud.crear_pedido(db, current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@api_router.get("/pedidos/{pedido_id}", response_model=schemas.PedidoResponse,
                summary="Obtener pedido", description="Obtener los detalles de un pedido específico por su ID",
                response_description="Detalles del pedido")
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(get_current_user)):
    pedido = crud.get_pedido(db, pedido_id, current_user.id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido
