from pydantic import BaseModel

# ==================== CARRITO ====================

class CarritoItem(BaseModel):
    producto_id: int
    cantidad: int

class CarritoResponse(BaseModel):
    id: int
    cliente_id: int
    items: list[CarritoItem]

    class Config:
        from_attributes = True

class ItemCarritoCreate(BaseModel):
    producto_id: int
    cantidad: int


class ItemCarritoUpdate(BaseModel):
    cantidad: int

# ==================== PEDIDOS ====================

class PedidoItem(BaseModel):
    producto_id: int
    cantidad: int

    class Config:
        from_attributes = True

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    detalles: list[PedidoItem]

    class Config:
        from_attributes = True
