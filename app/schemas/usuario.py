from typing import Optional

from pydantic import BaseModel, EmailStr

# ==================== USUARIOS ====================

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str
    es_admin: bool = False


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    es_admin: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    es_admin: bool
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Credentials(BaseModel):
    """Schema para credenciales de login (email + contraseña)."""
    email: EmailStr
    password: str
