Quieres documentación formal para tu API con JWT, roles, SQLite y Swagger personalizado. Milagro, alguien que sí estructura su proyecto. Me agrada. Aquí tienes tu **README.md** listo para copiar y pegar. Sin sarcasmo dentro, porque esto va para tu repositorio, no para terapia grupal.

---

# 🎓 API de Gestión de Estudiantes con FastAPI + JWT

API REST desarrollada con **FastAPI** que permite gestionar estudiantes con autenticación basada en JWT y control de roles (admin / usuario).

---

## 🚀 Tecnologías Utilizadas

* Python 3.10+
* FastAPI
* SQLite
* SQLAlchemy
* JWT (python-jose)
* Passlib (bcrypt)
* Swagger UI personalizado

---

## 📁 Estructura del Proyecto

```
📦 proyecto
 ┣ 📜 main.py        # Archivo principal (API y endpoints)
 ┣ 📜 auth.py        # Lógica de autenticación y JWT
 ┣ 📜 estudiantes.db # Base de datos SQLite (se crea automáticamente)
 ┗ 📜 README.md
```

---

## ⚙️ Instalación

### 1️⃣ Crear entorno virtual

```bash
python -m venv venv
```

Activar:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

---

### 2️⃣ Instalar dependencias

```bash
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt] python-multipart
```

---

### 3️⃣ Ejecutar el servidor

```bash
uvicorn main:app --reload
```

Servidor disponible en:

```
http://127.0.0.1:8000
```

---

## 🔐 Autenticación

La API usa **JWT (Bearer Token)**.

### Usuarios de prueba:

| Usuario | Contraseña | Rol     |
| ------- | ---------- | ------- |
| admin   | admin123   | admin   |
| user    | user123    | usuario |

---

### 🔑 Obtener Token

**POST** `/token`

Body (x-www-form-urlencoded):

```
username=admin
password=admin123
```

Respuesta:

```json
{
  "access_token": "TOKEN_GENERADO",
  "token_type": "bearer",
  "rol": "admin"
}
```

---

### 🔎 Verificar Token

**GET** `/verificar`

Header:

```
Authorization: Bearer TU_TOKEN
```

---

## 👨‍🎓 Endpoints de Estudiantes

### 🔍 Listar estudiantes

**GET** `/estudiantes`
Requiere usuario autenticado.

---

### 🔍 Obtener estudiante por ID

**GET** `/estudiantes/{id}`
Requiere usuario autenticado.

---

### ➕ Crear estudiante

**POST** `/estudiantes`
Solo rol **admin**

Body (form-data):

* nombre
* edad
* sexo
* correo
* telefono
* direccion
* carrera

---

### ✏️ Editar estudiante

**PUT** `/estudiantes/{id}`
Solo rol **admin**

---

### ❌ Eliminar estudiante

**DELETE** `/estudiantes/{id}`
Solo rol **admin**

---

## 🛡 Control de Roles

* `require_user` → Permite cualquier usuario autenticado.
* `require_admin` → Solo permite usuarios con rol `admin`.

---

## 🗄 Base de Datos

Se utiliza SQLite.

Archivo generado automáticamente:

```
estudiantes.db
```

Tabla creada:

```sql
CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    sexo TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    telefono TEXT NOT NULL,
    direccion TEXT NOT NULL,
    carrera TEXT NOT NULL
);
```

---

## 📘 Swagger Personalizado

Ruta:

```
/docs/admin
```

Interfaz estilizada con CSS personalizado.

---

## 🔒 Seguridad Implementada

* Autenticación JWT
* Hash de contraseñas con bcrypt
* Control de roles
* Protección de endpoints mediante Depends()

---

## 🧠 Flujo de Autenticación

1. Usuario envía credenciales a `/token`
2. Se valida contraseña con bcrypt
3. Se genera JWT con:

   * sub (username)
   * rol
   * exp (fecha de expiración)
4. Usuario usa el token en el header:

   ```
   Authorization: Bearer TOKEN
   ```
5. Dependencias validan autenticación y rol

---

## 🧪 Probar en Postman

1. POST → `/token`
2. Copiar `access_token`
3. En Headers:

   ```
   Authorization: Bearer TOKEN
   ```
4. Probar endpoints protegidos

---

## 👨‍💻 Autor

Industria TilinosDevelopers S.A de C.V. 
Ing. Tilino Developer Master.

---
