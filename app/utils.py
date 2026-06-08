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

from passlib.context import CryptContext
import os

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



"""Ejemplo de uso rápido (no usar en producción):"""
"""
if __name__ == "__main__":
    # Pequeña demostración / verificación rápida (no usar en producción).
    pw = "correcthorsebatterystaple"
    h = hash_password(pw)
    print("Hash:", h)
    print("Verifica (correcta):", verify_password(pw, h))
    print("Verifica (incorrecta):", verify_password("nope", h))

"""
