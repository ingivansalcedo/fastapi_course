import uuid
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.deps import requires_admin
from app.main import app
from app.models.categoria import Categoria

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_requires_admin():
    app.dependency_overrides[requires_admin] = lambda: SimpleNamespace(
        id=1,
        nombre="Admin Test",
        email="admin@test.local",
        is_active=True,
        es_admin=True,
    )
    yield
    app.dependency_overrides.pop(requires_admin, None)


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def categoria_id(db_session):
    categoria = Categoria(nombre=f"Categoria Test {uuid.uuid4().hex[:8]}")
    db_session.add(categoria)
    db_session.commit()
    db_session.refresh(categoria)
    return categoria.id


def test_obtener_todos_los_productos():
    response = client.get("/api/v1/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_producto_valido(categoria_id):
    producto_data = {
        "nombre": f"Laptop {uuid.uuid4().hex[:6]}",
        "descripcion": "Laptop de alto rendimiento",
        "precio": 999.99,
        "stock": 10,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    response = client.post("/api/v1/productos", json=producto_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == producto_data["nombre"]
    assert data["precio"] == producto_data["precio"]
    assert data["stock"] == producto_data["stock"]


def test_crear_producto_sin_nombre(categoria_id):
    producto_data = {
        "descripcion": "Producto sin nombre",
        "precio": 50.00,
        "stock": 5,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    response = client.post("/api/v1/productos", json=producto_data)
    assert response.status_code == 422


def test_crear_producto_precio_negativo(categoria_id):
    producto_data = {
        "nombre": "Producto",
        "descripcion": "Test",
        "precio": -10.00,
        "stock": 5,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    response = client.post("/api/v1/productos", json=producto_data)
    assert response.status_code == 400


def test_crear_producto_stock_negativo(categoria_id):
    producto_data = {
        "nombre": "Producto",
        "descripcion": "Test",
        "precio": 50.00,
        "stock": -5,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    response = client.post("/api/v1/productos", json=producto_data)
    assert response.status_code == 400


def test_actualizar_producto_valido(categoria_id):
    crear_payload = {
        "nombre": f"Producto Base {uuid.uuid4().hex[:6]}",
        "descripcion": "Base",
        "precio": 100.0,
        "stock": 5,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    crear_response = client.post("/api/v1/productos", json=crear_payload)
    assert crear_response.status_code == 201
    producto_id = crear_response.json()["id"]

    actualizar_payload = {
        "nombre": "Producto actualizado",
        "precio": 150.00,
        "stock": 20,
    }
    response = client.put(f"/api/v1/productos/{producto_id}", json=actualizar_payload)
    assert response.status_code == 200
    assert response.json()["nombre"] == "Producto actualizado"
    assert response.json()["stock"] == 20


def test_actualizar_producto_inexistente():
    producto_data = {
        "nombre": "Producto",
        "precio": 50.00,
    }
    response = client.put("/api/v1/productos/999999", json=producto_data)
    assert response.status_code == 404


def test_eliminar_producto_existente(categoria_id):
    crear_payload = {
        "nombre": f"Eliminar {uuid.uuid4().hex[:6]}",
        "descripcion": "Eliminar",
        "precio": 20.0,
        "stock": 2,
        "disponible": True,
        "categoria_id": categoria_id,
    }
    crear_response = client.post("/api/v1/productos", json=crear_payload)
    assert crear_response.status_code == 201
    producto_id = crear_response.json()["id"]

    response = client.delete(f"/api/v1/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Producto eliminado"}


def test_eliminar_producto_inexistente():
    response = client.delete("/api/v1/productos/999999")
    assert response.status_code == 404
