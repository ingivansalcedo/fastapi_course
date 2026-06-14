from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemas.categoria import CategoriaResponse

# ==================== PRODUCTOS ====================

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    disponible: bool = True
    categoria_id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True


class ProductoWithCategoria(ProductoResponse):
    categoria: Optional["CategoriaResponse"] = None

    class Config:
        from_attributes = True