from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.deps import get_db, requires_admin

api_router = APIRouter()

# ==================== ENDPOINTS CATEGORIAS ====================


@api_router.get("/categorias", response_model=list[schemas.CategoriaResponse],
                summary="Listar categorías", description="Obtener la lista de todas las categorías",
                response_description="Lista de categorías")
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categorias(db)


@api_router.get("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse,
                summary="Obtener categoría", description="Obtener los detalles de una categoría específica por su ID",
                response_description="Detalles de la categoría")
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


@api_router.get("/categorias/{categoria_id}/productos", response_model=list[schemas.ProductoResponse],
                summary="Listar productos por categoría", description="Obtener la lista de productos de una categoría específica",
                response_description="Lista de productos")
def listar_productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return crud.get_productos_by_categoria(db, categoria_id)


@api_router.post("/categorias", response_model=schemas.CategoriaResponse,
                 summary="Crear categoría", description="Crear una nueva categoría",
                 response_description="Categoría creada exitosamente")
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    existing = crud.get_categoria_by_nombre(db, categoria.nombre)
    if existing:
        raise HTTPException(status_code=400, detail="La categoría ya existe")
    return crud.create_categoria(db, categoria)


@api_router.put("/categorias/{categoria_id}", response_model=schemas.CategoriaResponse,
                summary="Actualizar categoría", description="Actualizar los detalles de una categoría existente",
                response_description="Categoría actualizada exitosamente")
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriaUpdate, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )
    try:
        return crud.update_categoria(db, categoria_id, categoria)
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@api_router.delete("/categorias/{categoria_id}",
                   summary="Eliminar categoría", description="Eliminar una categoría existente",
                   response_description="Categoría eliminada exitosamente")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db), current_user: schemas.UsuarioResponse = Depends(requires_admin)):

    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes: se requieren privilegios de administrador",
        )

    try:
        crud.delete_categoria(db, categoria_id)
        return {"mensaje": "Categoría eliminada"}
    except crud.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
