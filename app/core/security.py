import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "KblBeFYTrP5PrBZMkNDkFtT.liKKaoe"
    print("⚠️  ADVERTENCIA: SECRET_KEY no definida en .env. Usando clave por defecto (NO SEGURA).")

ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

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
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    )
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




"""Utilidades para el hash y verificación de contraseñas.

Este módulo utiliza passlib + bcrypt para generar hashes de contraseñas
de forma segura.

Notas:
- Esto realiza hashing (unidireccional), no cifrado reversible. Use hashing
    para almacenar contraseñas.
- bcrypt genera automáticamente una salt y la incluye dentro del hash.
- El coste de bcrypt (rounds) puede ajustarse con la variable de entorno
    `BCRYPT_ROUNDS` (por defecto: 12). Aumente los rounds para elevar
    el factor de trabajo.
- NO registre contraseñas en texto claro ni las almacene sin protección.
"""


# Permite ajustar el coste de bcrypt vía entorno (por defecto 12 rounds).
# Ejemplo (Windows PowerShell): $env:BCRYPT_ROUNDS = "14"
DEFAULT_BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", "12"))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=DEFAULT_BCRYPT_ROUNDS,
)

def hash_password(password: str) -> str:
    """
    Hashea una contraseña en texto plano usando bcrypt y devuelve el hash.

    Args:
        password: Contraseña en texto plano a hashear.

    Returns:
        Un hash bcrypt (incluye salt y coste) apto para almacenar.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña en texto plano frente a un hash bcrypt almacenado.

    Args:
        plain_password: La contraseña proporcionada por el usuario.
        hashed_password: El hash bcrypt almacenado con el que verificar.

    Returns:
        True si la contraseña coincide con el hash, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)

#Ejemplo de uso rápido (no usar en producción):
"""
if __name__ == "__main__":
    # Pequeña demostración / verificación rápida (no usar en producción).
    pw = "correcthorsebatterystaple"
    h = hash_password(pw)
    print("Hash:", h)
    print("Verifica (correcta):", verify_password(pw, h))
    print("Verifica (incorrecta):", verify_password("nope", h))

"""
