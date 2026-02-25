---

# API de Gestión de Estudiantes

API desarrollada con **FastAPI** que permite la gestión completa de estudiantes con autenticación basada en roles (`admin` y `user`), panel web y documentación protegida.

---

# ¿Qué hace esta API?

Esta aplicación permite:

## Administrador

* Ver todos los estudiantes
* Buscar estudiante por ID
* Crear estudiantes
* Actualizar estudiantes
* Eliminar estudiantes
* Acceder a Swagger personalizado protegido

## Usuario Normal

* Iniciar sesión
* Acceder a panel web
* Buscar estudiante por ID
* Visualizar lista de estudiantes

---

# Tecnologías Utilizadas

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Jinja2
* JWT (autenticación personalizada)
* Docker
* Docker Compose

---

# Estructura del Proyecto

```
mi-api-xd/
│
├── main.py
├── auth.py
├── estudiantes.db
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── README.md
│
├── templates/
│   ├── login.html
│   ├── panel_usuario.html
│   └── swagger_admin.html
│
└── venv/
```

---

# Requisitos

* Python 3.10 o superior
* pip
* Docker (opcional)
* Docker Compose (opcional)

---

# Ejecución en Entorno Local (VS Code)

## 1️⃣ Clonar el repositorio

```
git clone <https://github.com/Tilino22/MiApiEstudiantes>
cd mi-api-xd
```

---

## 2️⃣ Crear entorno virtual

```
python -m venv venv
```

Activar entorno:

Windows:

```
venv\Scripts\activate
```

Mac / Linux:

```
source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```
pip install -r requirements.txt
```

---

## 4️⃣ Ejecutar el servidor

```
uvicorn main:app --reload
```

Servidor disponible en:

```
http://127.0.0.1:8000
```

---

# Accesos

* Login:
  [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

* Swagger (solo admin):
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* Panel usuario:
  [http://127.0.0.1:8000/panel-usuario](http://127.0.0.1:8000/panel-usuario)

---

# Ejecutar con Docker

## Construir imagen

```
docker build -t api-estudiantes .
```

## Ejecutar contenedor

```
docker run -p 8000:8000 api-estudiantes
```

Acceder en:

```
http://localhost:8000
```

---

# Ejecutar con Docker Compose

```
docker compose up --build
```

Detener:

```
docker compose down
```

---

# Base de Datos

* Motor: SQLite
* Archivo: `estudiantes.db`
* Se crea automáticamente al iniciar la aplicación

---

# Seguridad

* Autenticación mediante JWT almacenado en cookie HTTPOnly
* Sistema de roles:

  * admin
  * user
* Swagger protegido solo para administradores

---

# Endpoints Principales

| Método | Endpoint          | Rol   |
| ------ | ----------------- | ----- |
| GET    | /estudiantes      | Admin |
| GET    | /estudiantes/{id} | Admin |
| POST   | /estudiantes      | Admin |
| PUT    | /estudiantes/{id} | Admin |
| DELETE | /estudiantes/{id} | Admin |

---

# Desarrollador

**Industria TilinosDevelopers S.A de C.V.**

**Autor:** Tilino Developer Master



