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
| `DEVELOPER` | Ver las tareas que tiene asignadas, comentar, y editar lo propio |

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
- **`409` antes que `403`.** Al cambiar el estado de una tarea se comprueba primero si
  la transición existe para alguien, y después si existe para ti. Al revés el mensaje
  mentiría: diría "no tienes permiso" cuando la verdad es "eso no se puede hacer".
- **Si no puedes ver una tarea, recibes `404`, no `403`.** Un `403` confirmaría que
  existe, y probando ids se reconstruiría la tabla.
- **`created_by` es historia; `project.manager_id` es autoridad.** Quién escribió una
  fila es un dato del pasado; los permisos se deciden con quién manda hoy.
- **El correo es identidad, no texto libre.** Se normaliza a minúsculas al entrar y la
  tabla tiene una restricción de unicidad, porque validarlo solo en el servicio deja
  una ventana de carrera entre la consulta y el `INSERT`.

---

## Endpoints

Todos bajo el prefijo **`/api/v1`**. Son 21.

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
| `GET` | `/tasks/` | Listar tareas, **filtradas según quién pregunta** | Autenticado |
| `GET` | `/tasks/{task_id}` | Obtener una tarea, si es visible para quien pregunta | Autenticado |
| `POST` | `/tasks/` | Crear tarea | Manager del proyecto o ADMIN |
| `PATCH` | `/tasks/{task_id}` | Editar título y descripción | Creador, manager del proyecto o ADMIN |
| `PATCH` | `/tasks/{task_id}/status` | Cambiar el estado | Depende de la transición |

**Qué ve cada quien en `GET /tasks/`:** un ADMIN, todas. Un MANAGER, las de los
proyectos que gestiona más las que tenga asignadas. Un DEVELOPER, solo las asignadas
a él. El filtro se aplica en la consulta, no después de traer las filas.

**Las transiciones de estado** son una máquina de estados, no un campo de texto. De
las nueve combinaciones posibles, dos son imposibles para cualquiera (`409`), tres son
el mismo estado (`409`) y las cuatro restantes dependen de quién pregunta: mover entre
`PENDING` e `IN_PROGRESS` lo puede hacer el asignado, el manager del proyecto o un
ADMIN; completar o reabrir, solo el manager o un ADMIN.

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

## Levantarlo con Docker

La forma rápida. Lo único que necesitas instalado es Docker.

```bash
git clone https://github.com/Fernando-03-Git/taskflow-api.git
cd taskflow-api
copy .env.example .env      # Windows.  En Linux o macOS: cp .env.example .env
docker compose up
```

Y ya está: **http://localhost:8000/docs**

Eso levanta dos contenedores —la API y un PostgreSQL 16— conectados en una red
privada. Las migraciones se aplican solas al arrancar, así que la base queda con
sus tablas sin que tengas que hacer nada.

Para cargar los usuarios de prueba, en otra terminal:

```bash
docker compose exec app python -m scripts.seed
```

Tres cosas que conviene saber:

- **Los datos sobreviven.** Viven en un volumen, no dentro del contenedor, así que
  `docker compose down` no los borra. Solo lo hace `docker compose down -v`.
- **PostgreSQL se publica en el 5433**, no en el 5432, para no chocar con uno que
  ya tengas instalado. Si quieres conectarte con psql o DBeaver, ese es el puerto.
- **El `.env` nunca entra a la imagen.** Lo excluye el `.dockerignore`, y la
  configuración se inyecta al arrancar el contenedor. La misma imagen sirve para
  desarrollo y para producción; lo único que cambia son las variables.

---

## Instalación manual

Si prefieres correrlo sin contenedores, contra tu propio PostgreSQL.

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

Crea seis usuarios de desarrollo: un ADMIN, dos MANAGER, dos DEVELOPER y uno
desactivado para probar ese caso. Es idempotente: se puede correr las veces que haga
falta y el resultado siempre es el mismo.

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

Esto no es un producto terminado: es un proyecto de aprendizaje, y prefiero decir qué
falta antes de que alguien lo descubra leyendo el código.

**Hecho**

- Autenticación con JWT y hash con bcrypt
- Roles aplicados endpoint por endpoint, con una fábrica de dependencias
- Autorización por propiedad en comentarios y en la edición de tareas
- Máquina de estados de las tareas: las nueve transiciones cubiertas, cada una con
  quién puede hacerla
- Visibilidad de tareas filtrada en la consulta según el rol de quien pregunta
- El correo como identidad: único en la base, normalizado a minúsculas
- Manejadores globales de excepciones, headers de seguridad, logging por petición
- Migraciones con Alembic
- Pruebas de autenticación y usuarios

**Pendiente**

Hay diez huecos conocidos —de seguridad, de modelo de datos y de consistencia de la
API— y varios pendientes de alcance como la paginación, el async y el despliegue.
Cada uno está documentado con qué pasa, qué implica y qué haría falta:

→ **[BACKLOG.md](BACKLOG.md)**

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
