# TaskFlow API

API REST para la gestión de proyectos y tareas colaborativas (estilo Jira simplificado), construida con **FastAPI** y **PostgreSQL**, con autenticación JWT y control de acceso por roles.

## Stack

| Capa | Tecnología |
|---|---|
| Framework | FastAPI |
| Base de datos | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (modelos tipados con `Mapped[]`) |
| Migraciones | Alembic |
| Validación | Pydantic v2 |
| Autenticación | JWT (python-jose) + hash de contraseñas con bcrypt |
| Pruebas | pytest + TestClient |

## Características

- **20 endpoints REST** en 5 módulos: autenticación, usuarios, proyectos, tareas y comentarios.
- **Autenticación JWT** con esquema Bearer.
- **Control de acceso por roles** (`ADMIN`, `MANAGER`, `DEVELOPER`) mediante una dependencia reutilizable (`require_role`).
- **Propiedad de los recursos protegida**: el creador de una tarea, proyecto o comentario se toma del token, nunca del cuerpo de la petición.
- **Desactivación lógica de usuarios** (soft delete) en lugar de borrado físico.
- **Respuestas de error uniformes** mediante manejadores globales de excepciones, sin exponer detalles internos en errores 500.
- **Headers de seguridad** y registro de tiempo de respuesta por petición mediante middleware.
- **Pruebas automatizadas** contra una base de datos PostgreSQL aislada.

## Arquitectura

Arquitectura en capas, con un módulo por recurso en cada capa:

```
main.py                     Configuración de la app: CORS, middleware, manejadores de errores
app/
├── api/v1/
│   ├── router.py           Registra los routers bajo /api/v1
│   └── endpoints/          Capa HTTP: rutas y dependencias de autenticación
├── services/               Lógica de negocio
├── schemas/                Modelos Pydantic de entrada y salida
├── models/                 Modelos SQLAlchemy
├── core/                   Configuración, seguridad (hash/JWT) y dependencias
├── db/                     Sesión y conexión a la base de datos
└── tests/                  Pruebas con pytest
alembic/                    Migraciones de base de datos
```

Flujo de una petición: **endpoint → service → model → PostgreSQL**. Los endpoints se mantienen delgados; la lógica y las validaciones de negocio viven en los servicios.

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Fernando-03-Git/taskflow-api.git
cd taskflow-api
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux / macOS
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
APP_NAME=TaskFlow
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://usuario:password@localhost/taskflow

# Opcionales (valores por defecto)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Aplicar migraciones

```bash
alembic upgrade head
```

### 6. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

## Documentación interactiva

Con el servidor en ejecución:

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

Para probar endpoints protegidos en Swagger: haz login en `POST /api/v1/auth/`, copia el `access_token` y pégalo en el botón **Authorize**.

## Endpoints

Todas las rutas usan el prefijo `/api/v1`.

| Módulo | Método | Ruta | Descripción | Acceso |
|---|---|---|---|---|
| Auth | POST | `/auth/` | Login y obtención del token | Público |
| Usuarios | GET | `/users/` | Listar usuarios | ADMIN |
| Usuarios | GET | `/users/{user_id}` | Obtener un usuario | ADMIN |
| Usuarios | POST | `/users/` | Crear usuario | ADMIN |
| Usuarios | PATCH | `/users/{user_id}` | Actualizar usuario | ADMIN |
| Usuarios | DELETE | `/users/{user_id}` | Desactivar usuario (soft delete) | ADMIN |
| Usuarios | PATCH | `/users/me/password` | Cambiar la contraseña propia | Autenticado |
| Proyectos | GET | `/projects/` | Listar proyectos | Autenticado |
| Proyectos | GET | `/projects/{project_id}` | Obtener un proyecto | Autenticado |
| Proyectos | POST | `/projects/` | Crear proyecto | ADMIN, MANAGER |
| Proyectos | PATCH | `/projects/{project_id}` | Actualizar proyecto | ADMIN, MANAGER |
| Tareas | GET | `/tasks/` | Listar tareas | Autenticado |
| Tareas | GET | `/tasks/{task_id}` | Obtener una tarea | Autenticado |
| Tareas | POST | `/tasks/` | Crear tarea | ADMIN, MANAGER |
| Tareas | PATCH | `/tasks/{task_id}` | Actualizar tarea | Autenticado |
| Comentarios | GET | `/comment/` | Listar comentarios | Autenticado |
| Comentarios | GET | `/comment/{comment_id}` | Obtener un comentario | Autenticado |
| Comentarios | POST | `/comment/` | Crear comentario | Autenticado |
| Comentarios | PATCH | `/comment/{comment_id}` | Editar comentario | Autenticado |
| Comentarios | DELETE | `/comment/{comment_id}` | Eliminar comentario | Autenticado |

### Formato de errores

Todas las respuestas de error siguen la misma estructura:

```json
{
  "error": true,
  "status_code": 404,
  "detail": "Descripción del error"
}
```

## Pruebas

Las pruebas corren contra una base de datos PostgreSQL separada. El nombre se obtiene de `DATABASE_URL` reemplazando `taskflow` por `taskflow_test`, así que primero crea esa base de datos:

```bash
createdb taskflow_test
```

Instala las dependencias de pruebas y ejecútalas:

```bash
pip install pytest httpx
pytest -v
```

Las tablas se crean al inicio de la sesión de pruebas y se eliminan al terminar. Cobertura actual:

- Login exitoso, contraseña incorrecta y email inexistente.
- Creación de usuario por un ADMIN autenticado.

## Próximos pasos

- [ ] Ampliar las pruebas a proyectos, tareas, comentarios y permisos por rol.
- [ ] Desplegar en Railway.
- [ ] Contenerizar con Docker.
- [ ] Integración continua con GitHub Actions (ejecutar las pruebas en cada push).
- [ ] Refresh tokens.

## Autor

**Fernando Esquivia Ortega** — Backend Developer (Python · FastAPI · PostgreSQL)

[GitHub](https://github.com/Fernando-03-Git) · [LinkedIn](https://linkedin.com/in/fernando-esquivia)
