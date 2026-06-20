from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)


class CategoriaWithProductos(CategoriaResponse):
    productos: List["ProductoResponse"] = []
    model_config = ConfigDict(from_attributes=True)
