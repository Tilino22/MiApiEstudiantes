# ==============================
# main.py
# ==============================

from fastapi import FastAPI, HTTPException, Form, Depends, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
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

class EstudianteOut(BaseModel):
    id: int
    nombre: str
    edad: str
    sexo: str
    correo: str
    telefono: str
    direccion: str
    carrera: str

    class Config:
        from_attributes = True

# ==============================
# FASTAPI
# ==============================

app = FastAPI(docs_url=None, redoc_url=None)

# ==============================
# DEPENDENCIA QUE LEE TOKEN DE COOKIE
# ==============================

def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="No autenticado")

    token = access_token.replace("Bearer ", "")
    payload = auth.verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload


def require_user(user: dict = Depends(get_current_user)):
    return user


def require_admin(user: dict = Depends(get_current_user)):
    if user["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo administradores")
    return user

# ==============================
# TOKEN PARA SWAGGER
# ==============================

@app.post("/token")
def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    access_token = auth.create_token(
        data={"sub": user["username"], "rol": user["rol"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ==============================
# LOGIN HTML
# ==============================

@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <html>
    <body style="font-family:Arial; text-align:center; margin-top:100px;">
        <h2>API Estudiantes</h2>
        <form method="post" action="/login-web">
            <input name="username" placeholder="Usuario" required/><br><br>
            <input name="password" type="password" placeholder="Contraseña" required/><br><br>
            <button type="submit">Entrar</button>
        </form>
    </body>
    </html>
    """

# ==============================
# LOGIN WEB (GENERA TOKEN Y LO GUARDA EN COOKIE)
# ==============================

@app.post("/login-web")
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

# ==============================
# PANEL USUARIO
# ==============================

@app.get("/panel-usuario", response_class=HTMLResponse)
def panel_usuario(current_user: dict = Depends(require_user)):
    db = SessionLocal()
    estudiantes = db.query(EstudianteDB).all()
    db.close()

    filas = ""
    for e in estudiantes:
        filas += f"""
        <tr>
            <td>{e.id}</td>
            <td>{e.nombre}</td>
            <td>{e.carrera}</td>
        </tr>
        """

    return f"""
    <html>
    <body style="font-family:Arial; padding:40px;">
        <h1>Panel Usuario</h1>
        <table border="1" cellpadding="10">
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Carrera</th>
            </tr>
            {filas}
        </table>
    </body>
    </html>
    """

# ==============================
# SWAGGER SOLO ADMIN
# ==============================

@app.get("/docs", include_in_schema=False)
def custom_swagger(current_user: dict = Depends(require_admin)):
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Panel Admin</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui'
            });
        </script>
    </body>
    </html>
    """)

# ==============================
# CRUD SOLO ADMIN
# ==============================

@app.post("/estudiantes")
def agregar_estudiante(
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
    db.close()
    return {"mensaje": "Estudiante agregado correctamente"}

@app.delete("/estudiantes/{id}")
def eliminar_estudiante(
    id: int,
    current_user: dict = Depends(require_admin)
):
    db = SessionLocal()
    estudiante = db.query(EstudianteDB).filter(EstudianteDB.id == id).first()

    if not estudiante:
        db.close()
        raise HTTPException(status_code=404, detail="No encontrado")

    db.delete(estudiante)
    db.commit()
    db.close()
    return {"mensaje": "Eliminado correctamente"}