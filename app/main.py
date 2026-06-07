import os

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
import crud, schemas


from database import DATABASE_URL, get_db

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
    

@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.get_productos(db)

@app.post("/productos", response_model=schemas.ProductoCreate)
def agregar_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db, producto)

@app.put("/productos/{producto_id}", response_model=schemas.ProductoCreate)
def actualizar_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    producto = crud.update_producto(db, producto_id, producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.delete_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

