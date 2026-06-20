import uuid

from fastapi.testclient import TestClient

from app import crud, schemas
from app.db.database import SessionLocal
from app.main import app

client = TestClient(app)


def test_login_invalido():
    response = client.post(
        "/login",
        data={"username": "invalid@example.com", "password": "invalid"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales inválidas"}


def test_login_valido():
    test_email = f"test_auth_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "123456"

    db = SessionLocal()
    try:
        crud.create_usuario(
            db,
            schemas.UsuarioCreate(
                nombre="Usuario Test Auth",
                email=test_email,
                password=test_password,
                es_admin=False,
            ),
        )
    finally:
        db.close()

    response = client.post(
        "/login",
        data={"username": test_email, "password": test_password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["access_token"] != ""


def test_ping_docs():
    response = client.get("/docs")
    assert response.status_code == 200
