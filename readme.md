# TaskFlow API

API REST para gestión de tareas y proyectos colaborativos, construida con FastAPI
y PostgreSQL.

Proyecto de aprendizaje con enfoque en **autorización** y **arquitectura en capas**:
no es un CRUD, es un sistema donde cada acción tiene reglas sobre quién puede hacerla.

---

## Stack

| | |
|---|---|
| **FastAPI** | Framework web |
| **PostgreSQL 16** | Base de datos |
| **SQLAlchemy 2.0** | ORM, con la API de `Mapped` / `mapped_column` |
| **Alembic** | Migraciones |
| **Pydantic v2** | Validación de entrada y salida |
| **JWT** (python-jose) | Autenticación |
| **bcrypt** | Hash de contraseñas |
| **pytest** | Pruebas |

---

## El modelo de autorización

Esta es la parte interesante del proyecto. Hay **tres capas** de control, y cada una
vive en un sitio distinto a propósito.

**1. Autenticación** — `get_current_user`, una dependencia de FastAPI que decodifica
el JWT y carga el usuario. Si el token falta o es inválido: `401`.

**2. Rol** — `require_role(["ADMIN", "MANAGER"])`, una **fábrica de dependencias**:
una función que devuelve la función que FastAPI inyecta. Vive en el decorador del
endpoint, porque el rol se puede decidir sin consultar la base de datos. Si el rol no
alcanza: `403`.

**3. Propiedad** — vive en el **servicio**, no en el endpoint, porque hace falta
cargar la fila para saber de quién es. Un usuario no puede editar el comentario de
otro aunque esté autenticado y tenga rol.

> **El criterio para decidir dónde va cada control:** si se puede decidir sin mirar la
> base de datos, va en el endpoint. Si hace falta saber de quién es el dato, va en el
> servicio.

### Roles

| Rol | Puede |
|---|---|
| `ADMIN` | Todo: gestionar usuarios, proyectos, cualquier tarea o comentario |
| `MANAGER` | Crear y editar proyectos y tareas |
| `DEVELOPER` | Ver, comentar, y editar lo propio |

### Decisiones de diseño

- **Los campos de propiedad nunca vienen del cliente.** `created_by` y `user_id` los
  inyecta el endpoint desde `current_user`, y los esquemas de entrada los omiten a
  propósito. No es un descuido: es lo que evita que alguien cree una tarea a nombre
  de otro.
- **Un endpoint por acción, no por campo.** Cambiar la contraseña tiene su propio
  endpoint (`PATCH /users/me/password`) en vez de ser un campo de `UserUpdate`,
  porque las reglas son distintas: pide la contraseña actual y no devuelve cuerpo.
- **Ningún esquema de respuesta expone el hash de la contraseña.** La columna es
  `String(60)` porque un hash de bcrypt mide exactamente 60 caracteres.

---

## Endpoints

Todos bajo el prefijo **`/api/v1`**. Son 20.

### Auth

| Método | Ruta | Qué hace | Requiere |
|---|---|---|---|
| `POST` | `/auth/` | Login: recibe email y contraseña, devuelve el access token | — |

### Usuarios

| Método | Ruta | Qué hace | Requiere |
|---|---|---|---|
| `GET` | `/users/` | Listar usuarios | ADMIN |
| `GET` | `/users/{user_id}` | Obtener un usuario | ADMIN |
| `POST` | `/users/` | Crear usuario | ADMIN |
| `PATCH` | `/users/{user_id}` | Actualizar nombre, email o rol | ADMIN |
| `PATCH` | `/users/me/password` | Cambiar mi propia contraseña (`204`) | Autenticado |
| `DELETE` | `/users/{user_id}` | Desactivar usuario (no borra la fila) | ADMIN |

### Proyectos

| Método | Ruta | Qué hace | Requiere |
|---|---|---|---|
| `GET` | `/projects/` | Listar proyectos | Autenticado |
| `GET` | `/projects/{project_id}` | Obtener un proyecto | Autenticado |
| `POST` | `/projects/` | Crear proyecto | ADMIN, MANAGER |
| `PATCH` | `/projects/{project_id}` | Actualizar proyecto | ADMIN, MANAGER |

### Tareas

| Método | Ruta | Qué hace | Requiere |
|---|---|---|---|
| `GET` | `/tasks/` | Listar tareas | Autenticado |
| `GET` | `/tasks/{task_id}` | Obtener una tarea | Autenticado |
| `POST` | `/tasks/` | Crear tarea | ADMIN, MANAGER |
| `PATCH` | `/tasks/{task_id}` | Editar título y descripción | Creador, manager del proyecto o ADMIN |

### Comentarios

| Método | Ruta | Qué hace | Requiere |
|---|---|---|---|
| `GET` | `/comment/` | Listar comentarios | Autenticado |
| `GET` | `/comment/{comment_id}` | Obtener un comentario | Autenticado |
| `POST` | `/comment/` | Crear comentario | Autenticado |
| `PATCH` | `/comment/{comment_id}` | Editar comentario | Solo el autor |
| `DELETE` | `/comment/{comment_id}` | Borrar comentario (`204`) | El autor o ADMIN |

### Raíz

| Método | Ruta | Qué hace |
|---|---|---|
| `GET` | `/` | Nombre, versión y modo de la aplicación |

---

## Lo que trae la aplicación además de los endpoints

- **CORS** configurado para el futuro frontend
- **Middleware de logging** que imprime método, ruta, código de estado y duración de
  cada petición
- **Headers de seguridad**: `X-Content-Type-Options`, `X-Frame-Options`,
  `X-XSS-Protection`
- **Dos manejadores globales de excepciones**: uno para los `HTTPException`
  intencionales, y uno para lo inesperado, que devuelve `500` **sin filtrar la traza
  al cliente**
- **Configuración fuera del código** con `pydantic-settings`, leyendo del `.env`

---

## Instalación

### 1. Clonar

```bash
git clone https://github.com/Fernando-03-Git/taskflow-api.git
cd taskflow-api
```

### 2. Entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Dependencias

```bash
pip install -r requirements.txt
```

### 4. Variables de entorno

Crear un `.env` en la raíz. **Nunca se sube al repositorio.**

```env
APP_NAME=TaskFlow
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=una_clave_larga_y_aleatoria
DATABASE_URL=postgresql://usuario:password@localhost/taskflow
```

### 5. Migraciones

```bash
alembic upgrade head
```

### 6. Correr

```bash
uvicorn main:app --reload
```

### 7. Datos de prueba

```bash
python -m scripts.seed
```

Crea cuatro usuarios de desarrollo (un ADMIN, dos MANAGER y un DEVELOPER). Es
idempotente: se puede correr las veces que haga falta.

---

## Documentación interactiva

Con el servidor corriendo:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## Pruebas

```bash
pytest
```

Hay pruebas de autenticación y de usuarios, con `conftest.py` usando
`app.dependency_overrides` para reemplazar la sesión de base de datos. Faltan las de
tareas y comentarios.

---

## Estado y límites conocidos

Esto no es un producto terminado: es un proyecto de aprendizaje y prefiero decir qué
falta antes de que alguien lo descubra leyendo el código.

**Hecho**

- Autenticación con JWT y hash con bcrypt
- Roles aplicados endpoint por endpoint
- Autorización por propiedad en comentarios y en la edición de tareas
- Manejadores globales de excepciones, headers de seguridad, logging
- Migraciones con Alembic
- Pruebas de auth y usuarios

**Pendiente, y por qué importa**

| Pendiente | Qué implica |
|---|---|
| **Paginación** | `GET /tasks/` y `GET /users/` devuelven todo. Con muchos registros, la respuesta pesa demasiado |
| **Visibilidad por proyecto** | Hoy cualquier usuario autenticado ve todas las tareas. Debería ver solo las de sus proyectos |
| **Validación de transiciones de estado** | El `status` de una tarea no tiene máquina de estados: falta definir qué cambios son válidos y quién los puede hacer |
| **Unicidad del email en la base de datos** | Se valida en el servicio, pero sin restricción en la tabla hay una ventana de carrera |
| **Revocación de sesiones** | Un token emitido antes de un cambio de contraseña sigue siendo válido hasta que vence |
| **Capa de repositorio** | Los servicios consultan el ORM directamente, y lanzan `HTTPException`, así que están acoplados a HTTP |
| **Async** | Todo es sincrónico. Con SQLAlchemy síncrono es la decisión correcta, pero limita la concurrencia |
| **Despliegue** | Solo corre en local |

**No hay registro público de usuarios a propósito.** Los crea un ADMIN. Es una
herramienta interna, no un SaaS.

---

## Estructura

```
app/
├── api/v1/
│   ├── endpoints/      # Solo traducen HTTP: reciben, delegan, devuelven
│   └── router.py       # Agrupa los routers por recurso
├── core/
│   ├── config.py       # pydantic-settings
│   ├── dependencies.py # get_current_user, require_role
│   └── security.py     # Hash de contraseñas, firma y lectura del JWT
├── db/
│   ├── deps.py         # get_db: una sesión por petición
│   └── session.py      # Motor y Base
├── models/             # Las tablas (SQLAlchemy)
├── schemas/            # El contrato con el exterior (Pydantic)
├── services/           # Las reglas de negocio
└── tests/
alembic/                # Migraciones
scripts/seed.py         # Datos de desarrollo
main.py                 # Aplicación, middleware, manejadores
```

---

## Autor

**Fernando Esquivia Ortega** — Ingeniería de Software, UNIMINUTO · Medellín, Colombia
