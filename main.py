from fastapi import FastAPI, HTTPException, Form, Depends, Cookie, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import auth

# ==============================
# BASE DE DATOS
# ==============================

DATABASE_URL = "sqlite:///./estudiantes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class EstudianteDB(Base):
    __tablename__ = "estudiantes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    carrera = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# ==============================
# MODELOS PYDANTIC
# ==============================

class EstudianteBase(BaseModel):
    nombre: str
    edad: int
    sexo: str
    correo: str
    telefono: str
    direccion: str
    carrera: str

class EstudianteCreate(EstudianteBase):
    pass

class EstudianteOut(EstudianteBase):
    id: int

    class Config:
        from_attributes = True

# ==============================
# FASTAPI
# ==============================

app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory="templates")

# ==============================
# AUTH
# ==============================

def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")

    token = access_token.replace("Bearer ", "")
    payload = auth.verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload

def require_admin(user: dict = Depends(get_current_user)):
    if user["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
    return user

def require_normal_user(user: dict = Depends(get_current_user)):
    if user["rol"] != "user":
        raise HTTPException(status_code=403, detail="Solo usuarios normales")
    return user

# ==============================
# CRUD ESTUDIANTES (SOLO ADMIN)
# ==============================

@app.get("/estudiantes", response_model=list[EstudianteOut])
def obtener_estudiantes(current_user: dict = Depends(require_admin)):
    db = SessionLocal()
    estudiantes = db.query(EstudianteDB).all()
    db.close()
    return estudiantes


@app.get("/estudiantes/{id}", response_model=EstudianteOut)
def obtener_estudiante(id: int, current_user: dict = Depends(require_admin)):
    db = SessionLocal()
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()
    db.close()

    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return estudiante


@app.post("/estudiantes", response_model=EstudianteOut)
def crear_estudiante(
    nombre: str = Form(...),
    edad: int = Form(...),
    sexo: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    carrera: str = Form(...),
    current_user: dict = Depends(require_admin)
):
    db = SessionLocal()

    nuevo = EstudianteDB(
        nombre=nombre,
        edad=edad,
        sexo=sexo,
        correo=correo,
        telefono=telefono,
        direccion=direccion,
        carrera=carrera
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.close()

    return nuevo


@app.put("/estudiantes/{id}", response_model=EstudianteOut)
def actualizar_estudiante(
    id: int,
    nombre: str = Form(...),
    edad: int = Form(...),
    sexo: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    direccion: str = Form(...),
    carrera: str = Form(...),
    current_user: dict = Depends(require_admin)
):
    db = SessionLocal()
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        db.close()
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    estudiante.nombre = nombre
    estudiante.edad = edad
    estudiante.sexo = sexo
    estudiante.correo = correo
    estudiante.telefono = telefono
    estudiante.direccion = direccion
    estudiante.carrera = carrera

    db.commit()
    db.refresh(estudiante)
    db.close()

    return estudiante


@app.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, current_user: dict = Depends(require_admin)):
    db = SessionLocal()
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        db.close()
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    db.delete(estudiante)
    db.commit()
    db.close()

    return {"mensaje": "Estudiante eliminado correctamente"}

# ==============================
# LOGIN Y PANEL (OCULTOS EN SWAGGER)
# ==============================

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login-web", include_in_schema=False)
def login_web(username: str = Form(...), password: str = Form(...)):
    user = auth.authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token = auth.create_token(
        data={"sub": user["username"], "rol": user["rol"]}
    )

    response = RedirectResponse(
        url="/docs" if user["rol"] == "admin" else "/panel-usuario",
        status_code=302
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True
    )

    return response


@app.get("/panel-usuario", response_class=HTMLResponse, include_in_schema=False)
def panel_usuario(
    request: Request,
    buscar_id: int = None,
    current_user: dict = Depends(require_normal_user)
):
    db = SessionLocal()

    estudiantes = db.query(EstudianteDB).all()
    estudiante_encontrado = None
    buscar_realizado = False

    if buscar_id:
        buscar_realizado = True
        estudiante_encontrado = db.query(EstudianteDB).filter(
            EstudianteDB.id == buscar_id
        ).first()

    db.close()

    return templates.TemplateResponse("panel_usuario.html", {
        "request": request,
        "estudiantes": estudiantes,
        "usuario": current_user.get("sub"),
        "estudiante_encontrado": estudiante_encontrado,
        "buscar_realizado": buscar_realizado
    })

# ==============================
# SWAGGER SOLO ADMIN
# ==============================

@app.get("/docs", include_in_schema=False)
def custom_swagger(request: Request, current_user: dict = Depends(require_admin)):
    return templates.TemplateResponse("swagger_admin.html", {"request": request})