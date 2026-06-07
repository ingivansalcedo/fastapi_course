from pydantic import BaseModel
from typing import List, Optional


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
    categoria: Optional[CategoriaResponse] = None

    class Config:
        from_attributes = True


# ==================== USUARIOS ====================

class UsuarioBase(BaseModel):
    nombre: str
    email: str


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

