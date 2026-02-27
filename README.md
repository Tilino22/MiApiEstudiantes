# API Gestión de Estudiantes v3.2

API REST desarrollada con FastAPI para la gestión de estudiantes con:

* Autenticación por API Key generada dinámicamente
* Control de roles (`admin`, `usuario`)
* Base de datos SQLite real con SQLAlchemy
* CRUD completo protegido

---

# Tecnologías

* FastAPI 0.110.0
* Uvicorn 0.29.0
* SQLAlchemy 2.0.29
* SQLite
* Passlib + Bcrypt
* Docker

---

# Clonar el Repositorio

Si deseas obtener el proyecto desde GitHub:

```
git clone https://github.com/Tilino22/Api_Estudiantes.git
cd mi-api-xd
```

Asegúrate de estar dentro del directorio del proyecto antes de continuar.

---

# Estructura del Proyecto

```
mi-api-xd/
│
├── main.py
├── auth.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── estudiantes.db (se crea automáticamente)
└── README.md
```

---

# Base de Datos

Motor: SQLite
Archivo: `estudiantes.db`
Se crea automáticamente al iniciar la aplicación.

Modelo Estudiante:

* id (Integer, Primary Key)
* nombre (String)
* edad (Integer)
* sexo (String)
* correo (String)
* telefono (String)
* direccion (String)
* carrera (String)
* usuario_id (Integer, opcional)

---

# Autenticación

La API usa autenticación mediante API Key enviada en el header:

```
X-API-Key: tu_api_key
```

⚠ No se permite enviar la API Key por URL.
Si se detecta en query params, se devuelve error 400.

---

# Usuario Administrador por Defecto

```
username: admin
password: admin123
rol: admin
```

La API Key se genera al iniciar sesión.

---

# Flujo de Uso

## 1️⃣ Registrar Usuario

POST `/registro`

Form-data:

* username
* password
* rol (opcional, por defecto "usuario")

---

## 2️⃣ Login

POST `/login`

Form-data:

* username
* password

Respuesta:

```
{
  "mensaje": "Login exitoso",
  "username": "admin",
  "rol": "admin",
  "api_key": "pk_xxxxxxxxx"
}
```

Guarda esa `api_key`.

---

## 3️⃣ Usar Endpoints Protegidos

En cada request protegida debes enviar:

```
X-API-Key: pk_xxxxxxxxx
```

---

# Endpoints

## Público

### GET /

Verifica que la API esté funcionando.

Disponible en:

```
http://localhost:8000
```

---

## Documentación Swagger

Disponible en:

```
http://localhost:8000/docs
```

Desde Swagger puedes probar todos los endpoints agregando el header `X-API-Key`.

---

## Protegidos

### GET /estudiantes

Lista todos los estudiantes.
Requiere API Key válida.

---

### GET /estudiantes/{id}

Obtiene estudiante por ID.

---

### POST /estudiantes

Crea estudiante.

Form-data requerido:

* id
* nombre
* edad
* sexo
* correo
* telefono
* direccion
* carrera
* usuario_id (opcional)

---

### PUT /estudiantes/{id}

Actualiza estudiante existente.
Mismos campos que creación.

---

### DELETE /estudiantes/{id}

Elimina estudiante.
Requiere rol `admin`.

---

# Ejecutar en Local

## 1. Crear entorno virtual

Windows:

```
python -m venv .venv
.venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instalar dependencias

```
pip install -r requirements.txt
```

## 3. Ejecutar servidor

```
uvicorn main:app --reload
```

Servidor disponible en:

```
http://localhost:8000
```

Documentación:

```
http://localhost:8000/docs
```

---

# Ejecutar con Docker

## Construir imagen

```
docker build -t api-estudiantes .
```

## Ejecutar contenedor

```
docker run -d --name api_estudiantes -p 8000:8000 api-estudiantes
```

Acceder en:

```
http://localhost:8000
```

Swagger:

```
http://localhost:8000/docs
```

---

# Ejecutar con Docker Compose

Levantar:

```
docker compose up -d
```

Detener:

```
docker compose down
```

La aplicación estará disponible en:

```
http://localhost:8000
```

---

# Seguridad Implementada

* Passwords encriptados con Bcrypt
* API Key generada dinámicamente al hacer login
* Validación de usuario activo
* Restricción de eliminación solo para rol admin
* Bloqueo de API Key en query params

---

# Versión

v3.2
Autenticación por API Key dinámica + base de datos SQLite real.

---

# Desarrollador

Industria TilinosDevelopers S.A de C.V.
Autor: Tilino Developer Master

