from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

# ==============================
# CONFIG
# ==============================

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================
# USUARIOS SIMULADOS
# ==============================

usuarios = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),
        "rol": "admin"
    },
    "user": {
        "username": "user",
        "password": pwd_context.hash("user123"),
        "rol": "user"
    }
}

# ==============================
# MODELO TOKEN
# ==============================

class Token(BaseModel):
    access_token: str
    token_type: str

# ==============================
# FUNCIONES
# ==============================

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str):
    user = usuarios.get(username)
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None