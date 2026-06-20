from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1 import auth
from app.api.v1.api import api_router
from app.deps import get_db

app = FastAPI(
    title="E-commerce API",
    description="""
        API para un sistema de comercio electrónico con FastAPI y SQLAlchemy
        - Gestión de usuarios (registro, login, roles)
        - CRUD de productos y categorías
        - Carrito de compras con validación de stock
        - Procesamiento de pedidos con control de inventario
        - Seguridad con OAuth2 y JWT
        - Documentación automática con OpenAPI
    """,
    version="1.0.0",
    contact={
        "name": "Ivan Salcedo",
        "email": "ingivansalcedo@yahoo.com.co",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

@app.post("/login", response_model=auth.schemas.Token)
def login_alias(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth.login(form_data=form_data, db=db)

app.include_router(api_router, prefix="/api/v1")
