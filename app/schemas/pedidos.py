from pydantic import BaseModel, ConfigDict

# ==================== CARRITO ====================

class CarritoItem(BaseModel):
    producto_id: int
    cantidad: int

class CarritoResponse(BaseModel):
    id: int
    cliente_id: int
    items: list[CarritoItem]
    model_config = ConfigDict(from_attributes=True)

class ItemCarritoCreate(BaseModel):
    producto_id: int
    cantidad: int


class ItemCarritoUpdate(BaseModel):
    cantidad: int

# ==================== PEDIDOS ====================

class PedidoItem(BaseModel):
    producto_id: int
    cantidad: int
    model_config = ConfigDict(from_attributes=True)

class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    detalles: list[PedidoItem]
    model_config = ConfigDict(from_attributes=True)
