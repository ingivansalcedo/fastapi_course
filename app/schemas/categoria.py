from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.producto import ProductoResponse

# ==================== CATEGORIAS ====================

class CategoriaBase(BaseModel):
    nombre: str


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    nombre: Optional[str] = None


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


class CategoriaWithProductos(CategoriaResponse):
    productos: List["ProductoResponse"] = []

    class Config:
        from_attributes = True
