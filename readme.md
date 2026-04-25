# TaskFlow API 🚀

Sistema de gestión de tareas y proyectos colaborativos.
API REST construida con FastAPI y PostgreSQL.

## Stack

- **FastAPI** — framework principal
- **PostgreSQL** — base de datos
- **SQLAlchemy** — ORM
- **Alembic** — migraciones
- **Pydantic v2** — validación de datos

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/Fernando-03-Git/taskflow-api.git
cd taskflow-api
```

2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
# Crear archivo .env con estas variables
APP_NAME=TaskFlow
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://usuario:password@localhost/taskflow
```

5. Aplicar migraciones
```bash
alembic upgrade head
```

6. Correr el servidor
```bash
uvicorn main:app --reload
```

## Documentación

Una vez corriendo, entrá a: http://localhost:8000/docs

## Estado actual

⚠️ Versión en desarrollo — sin autenticación todavía.

## Próximamente

- JWT con roles (ADMIN, MANAGER, DEVELOPER)
- Manejo de errores profesional
- Testing con pytest
- Despliegue en Railway