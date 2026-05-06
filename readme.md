# TaskFlow API 🚀

API REST para gestión de tareas y proyectos colaborativos,
construida con FastAPI y PostgreSQL.

## Stack

- **FastAPI** — framework principal
- **PostgreSQL 16** — base de datos
- **SQLAlchemy** — ORM
- **Alembic** — migraciones
- **Pydantic v2** — validación de datos
- **JWT** — autenticación y autorización

## Características implementadas

- 19 endpoints REST organizados por módulos
  (usuarios, proyectos, tareas, comentarios)
- Autenticación con JWT (access token + refresh token)
- Sistema de roles: ADMIN · MANAGER · DEVELOPER
- Validación de datos con Pydantic v2 en todos los módulos
- Migraciones de base de datos con Alembic
- Arquitectura en capas: routers → endpoints → services → models

## Instalación

### 1. Clonar el repositorio

\`\`\`bash
git clone https://github.com/Fernando-03-Git/taskflow-api.git
cd taskflow-api
\`\`\`

### 2. Crear entorno virtual

\`\`\`bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

\`\`\`env
APP_NAME=TaskFlow
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://usuario:password@localhost/taskflow
\`\`\`

### 5. Aplicar migraciones

\`\`\`bash
alembic upgrade head
\`\`\`

### 6. Correr el servidor

\`\`\`bash
uvicorn main:app --reload
\`\`\`

## Documentación

Con el servidor corriendo, accedé a la documentación interactiva:

- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

## Endpoints

| Módulo | Método | Ruta | Descripción |
|---|---|---|---|
| Auth | POST | /auth/register | Registro de usuario |
| Auth | POST | /auth/login | Login y obtención de token |
| Auth | POST | /auth/refresh | Refresh token |
| Usuarios | GET | /users/ | Listar usuarios |
| Usuarios | GET | /users/{id} | Obtener usuario |
| Usuarios | PUT | /users/{id} | Actualizar usuario |
| Usuarios | DELETE | /users/{id} | Eliminar usuario |
| Proyectos | POST | /projects/ | Crear proyecto |
| Proyectos | GET | /projects/ | Listar proyectos |
| Proyectos | GET | /projects/{id} | Obtener proyecto |
| Proyectos | PUT | /projects/{id} | Actualizar proyecto |
| Proyectos | DELETE | /projects/{id} | Eliminar proyecto |
| Tareas | POST | /tasks/ | Crear tarea |
| Tareas | GET | /tasks/ | Listar tareas |
| Tareas | GET | /tasks/{id} | Obtener tarea |
| Tareas | PUT | /tasks/{id} | Actualizar tarea |
| Tareas | DELETE | /tasks/{id} | Eliminar tarea |
| Comentarios | POST | /comments/ | Crear comentario |
| Comentarios | GET | /comments/{task_id} | Listar comentarios |

## En progreso

- Testing con pytest
- Despliegue en Railway
