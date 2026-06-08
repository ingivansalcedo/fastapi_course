import os

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from . import crud, schemas
from fastapi import HTTPException


from app.database import DATABASE_URL, get_db

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok", "database_url": DATABASE_URL}


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    

# ==================== ENDPOINTS PRODUCTOS ====================


@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.get_productos(db)


@app.post("/productos", response_model=schemas.ProductoResponse)
def agregar_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_producto(db, producto)
    except crud.InvalidDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.put("/productos/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_producto(db, producto_id, producto)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except crud.InvalidDataError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_producto(db, producto_id)
        return {"mensaje": "Producto eliminado"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


# ==================== ENDPOINTS CATEGORIAS ====================


@app.get("/categorias", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)


@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@app.get("/categorias/{categoria_id}/productos", response_model=list[schemas.ProductoResponse])
def listar_productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return crud.get_productos_by_categoria(db, categoria_id)


@app.post("/categorias", response_model=schemas.CategoriaResponse)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    existing = crud.get_categoria_by_nombre(db, categoria.nombre)
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    return crud.create_categoria(db, categoria)


@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse)
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_categoria(db, categoria_id, categoria)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@app.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_categoria(db, categoria_id)
        return {"mensaje": "Categoría eliminada"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

# ==================== ENDPOINTS USUARIOS ====================



@app.get("/usuarios", response_model=list[schemas.UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    print("Obteniendo usuarios...")
    return crud.get_usuarios(db)

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/usuarios", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except crud.DuplicateUserError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        crud.delete_usuario(db, usuario_id)
        return {"mensaje": "Usuario eliminado"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

