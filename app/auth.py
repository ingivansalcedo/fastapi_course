from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "KblBeFYTrP5PrBZMkNDkFtT.liKKaoe")
"""Clave secreta para firmar tokens JWT. Lee desde .env, usa default solo en desarrollo."""

if not os.getenv("SECRET_KEY"):
    print("⚠️  ADVERTENCIA: SECRET_KEY no definida en .env. Usando clave por defecto (NO SEGURA).")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crea un token JWT con la información proporcionada y una expiración opcional.

    Args:
        data: Un diccionario con los datos a incluir en el token (ej. {"sub": "usuario1"}).
        expires_delta: Tiempo de expiración del token (por defecto 30 minutos).

    Returns:
        Un token JWT como string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verifica un token JWT y devuelve su contenido si es válido.

    Args:
        token: El token JWT a verificar.

    Returns:
        Un diccionario con el contenido del token si es válido.

    Raises:
        JWTError: Si el token es inválido, expirado o malformado.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload