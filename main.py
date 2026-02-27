# ==========================================================
# MAIN.PY - FORMULARIO + API KEY + BASE DE DATOS REAL
# ==========================================================

from fastapi import FastAPI, HTTPException, Depends, status, Security, Form
from fastapi.security import APIKeyHeader
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Request
import auth

app = FastAPI(
    title="API Gestión de Estudiantes",
    version="3.2"
)

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ==========================================================
# CONFIGURACIÓN BASE DE DATOS
# ==========================================================

DATABASE_URL = "sqlite:///./estudiantes.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class EstudianteDB(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    carrera = Column(String, nullable=False)
    usuario_id = Column(Integer, nullable=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================
# DEPENDENCIAS SEGURIDAD (NO TOCADAS)
# ==========================================================

def get_current_user(
    request: Request,
    api_key: str = Security(api_key_header)
):
    # Bloquear si intentan enviar token por URL
    if "api_key" in request.query_params or "X-API-Key" in request.query_params:
        raise HTTPException(
            status_code=400,
            detail="Error pa, no eres un Tilino_Developer"
        )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere API Key en header X-API-Key"
        )

    user = auth.authenticate_with_api_key(api_key)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida o usuario inactivo"
        )

    return user

def admin_required(user: dict = Depends(get_current_user)):
    if user["rol"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador"
        )
    return user

# ==========================================================
# ENDPOINTS PÚBLICOS (NO TOCADOS)
# ==========================================================

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}

@app.post("/registro")
def registrar(
    username: str = Form(...),
    password: str = Form(...),
    rol: str = Form("usuario")
):
    nuevo = auth.create_user(username, password, rol)

    if not nuevo:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return nuevo

@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    resultado = auth.login_user(username, password)

    if not resultado:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "mensaje": "Login exitoso",
        "username": resultado["username"],
        "rol": resultado["rol"],
        "api_key": resultado["api_key"]
    }

# ==========================================================
# CRUD ESTUDIANTES (ACTUALIZADO)
# ==========================================================

@app.get("/estudiantes")
def listar_estudiantes(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(EstudianteDB).all()

@app.get("/estudiantes/{id}")
def obtener_estudiante(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail="No encontrado")

    return estudiante

@app.post("/estudiantes")
def crear_estudiante(
    id: int = Form(...),
    nombre: str = Form(...),
    edad: int = Form(...),
    sexo: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    carrera: str = Form(...),
    usuario_id: int = Form(None),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existente = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if existente:
        raise HTTPException(status_code=400, detail="ID ya existe")

    nuevo = EstudianteDB(
        id=id,
        nombre=nombre,
        edad=edad,
        sexo=sexo,
        correo=correo,
        telefono=telefono,
        direccion=direccion,
        carrera=carrera,
        usuario_id=usuario_id
    )

    db.add(nuevo)
    db.commit()

    return {
        "mensaje": "Estudiante creado",
        "creado_por": user["username"]
    }

@app.put("/estudiantes/{id}")
def actualizar_estudiante(
    id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    sexo: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    carrera: str = Form(...),
    usuario_id: int = Form(None),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail="No encontrado")

    estudiante.nombre = nombre
    estudiante.edad = edad
    estudiante.sexo = sexo
    estudiante.correo = correo
    estudiante.telefono = telefono
    estudiante.direccion = direccion
    estudiante.carrera = carrera
    estudiante.usuario_id = usuario_id

    db.commit()

    return {"mensaje": "Estudiante actualizado"}

@app.delete("/estudiantes/{id}")
def eliminar_estudiante(
    id: int,
    user: dict = Depends(admin_required),
    db: Session = Depends(get_db)
):
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail="No encontrado")

    db.delete(estudiante)
    db.commit()

    return {"mensaje": "Estudiante eliminado"}