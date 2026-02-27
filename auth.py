# ==========================================================
# AUTH.PY - AUTENTICACIÓN PROFESIONAL CON LOGIN + API KEY
# ==========================================================

from passlib.context import CryptContext
from typing import Optional, Dict, Any
import secrets

# ==========================================================
# CONFIGURACIÓN
# ==========================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==========================================================
# BASE DE DATOS SIMULADA
# ==========================================================

usuarios = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),
        "rol": "admin",
        "activo": True,
        "api_key": None
    }
}

# ==========================================================
# UTILIDADES
# ==========================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generar_api_key() -> str:
    return f"pk_{secrets.token_urlsafe(32)}"

# ==========================================================
# FUNCIONES PRINCIPALES
# ==========================================================

def create_user(username: str, password: str, rol: str = "usuario"):
    if username in usuarios:
        return None

    usuarios[username] = {
        "username": username,
        "password": hash_password(password),
        "rol": rol,
        "activo": True,
        "api_key": None
    }

    return {
        "username": username,
        "rol": rol,
        "activo": True
    }

def login_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    user = usuarios.get(username)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    if not user["activo"]:
        return None

    # Genera nueva API Key al iniciar sesión
    nueva_key = generar_api_key()
    user["api_key"] = nueva_key

    return {
        "username": user["username"],
        "rol": user["rol"],
        "api_key": nueva_key
    }

def authenticate_with_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    for user in usuarios.values():
        if user["api_key"] == api_key and user["activo"]:
            return {
                "username": user["username"],
                "rol": user["rol"],
                "activo": user["activo"]
            }
    return None