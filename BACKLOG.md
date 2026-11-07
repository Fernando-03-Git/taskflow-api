# BACKLOG — TaskFlow

Lo que sé que falta, y por qué todavía no está.

Cada entrada dice **qué pasa**, **qué implica** y **qué haría falta**. Es un proyecto
de aprendizaje en construcción: prefiero dejar escritos los límites a que alguien los
descubra leyendo el código.

Actualizado: 7 de noviembre de 2026.

---

## Seguridad

### 1. El token de un usuario desactivado sigue siendo válido

**Qué pasa.** `get_current_user` carga al usuario por el `sub` del token y no mira
`is_active`.

**Qué implica.** Desactivar a alguien con `DELETE /users/{id}` no le corta la sesión:
su token sigue entrando hasta que vence. Con la expiración por defecto, media hora de
acceso para alguien a quien acabas de sacar.

**Qué haría falta.** Una comprobación de `is_active` en `get_current_user`, con `401`.
Es una línea, pero pasa por los 21 endpoints a la vez, así que merece sus propias
pruebas antes de tocarla.

**Relacionado.** No hay revocación de sesiones en general: cambiar la contraseña
tampoco invalida los tokens ya emitidos.

### 2. Crear y editar proyectos no valida propiedad

**Qué pasa.** `POST /projects/` y `PATCH /projects/{id}` solo exigen rol `ADMIN` o
`MANAGER`. El `manager_id` llega en el cuerpo de la petición y nadie comprueba quién
la manda.

**Qué implica.** Un MANAGER puede crear un proyecto a nombre de otro. Y puede editar
un proyecto ajeno poniéndose a sí mismo como manager, con lo que se queda con el
control de las tareas de ese proyecto.

**Qué haría falta.** La misma validación de propiedad que ya tienen tareas y
comentarios, en el servicio. Y antes de eso, una decisión: si un MANAGER debería poder
crear proyectos o solo el ADMIN.

### 3. Enumeración de recursos por el código de estado

**Qué pasa.** `create_task` responde `404` si el proyecto no existe y `403` si existe
pero no es tuyo.

**Qué implica.** Probando ids se puede averiguar qué proyectos existen sin tener
acceso a ninguno.

**Qué haría falta.** Devolver `404` en los dos casos. En tareas ya se hace así
(`get_task_visible`); falta aplicar el mismo criterio en proyectos.

---

## Modelo de datos

### 4. No existe la pertenencia a un proyecto

**Qué pasa.** La única relación entre una persona y un proyecto es
`projects.manager_id`. No hay tabla de miembros.

**Qué implica.** Dos cosas. No se puede validar que el asignado de una tarea tenga
algo que ver con el proyecto: hoy se le puede asignar a cualquier usuario del sistema.
Y la visibilidad de un DEVELOPER solo puede basarse en las tareas que tiene asignadas,
no en los proyectos a los que pertenece, porque esa información no existe.

**Qué haría falta.** Una tabla `project_members`. Es funcionalidad nueva, no un
arreglo, y arrastra decisiones: quién añade miembros, si tienen un rol dentro del
proyecto, qué pasa con las tareas de alguien que sale.

### 5. Los tipos enum de PostgreSQL conservan el nombre viejo

**Qué pasa.** `tasks.status` y `projects.status` siguen usando un único tipo de
PostgreSQL llamado `status`, de cuando las dos clases de Python se llamaban igual. El
código ya declara `TaskStatus` y `ProjectStatus` por separado.

**Qué implica.** Funciona porque los valores coinciden, pero las dos tablas comparten
el mismo tipo en la base: añadir un estado a las tareas se lo añade también a los
proyectos. Era justo lo que la separación de clases buscaba evitar.

**Qué haría falta.** Una migración que cree los dos tipos y mueva cada columna.
Alembic la detecta pero la genera mal: el `alter_column` no crea el tipo, así que
falla al aplicarla.

### 6. `created_at` se rellena desde Python, no desde la base

**Qué pasa.** Los modelos usan `default=func.now()`, que aplica SQLAlchemy antes de
mandar el `INSERT`. La columna no tiene valor por omisión en PostgreSQL.

**Qué implica.** Cualquier inserción que no pase por SQLAlchemy falla por `NOT NULL`:
un script SQL, una migración de datos, otro servicio conectado a la misma base.

**Qué haría falta.** Cambiar a `server_default` y su migración correspondiente.

---

## Consistencia de la API

### 7. No hay forma de reactivar un usuario

**Qué pasa.** `DELETE /users/{id}` desactiva, pero `UserUpdate` no incluye
`is_active` y no existe otro endpoint que lo haga.

**Qué implica.** Desactivar es irreversible desde el API. La única salida es tocar la
base a mano o volver a correr el script de siembra.

**Qué haría falta.** Un endpoint de reactivación para ADMIN, hermano del `DELETE`.

### 8. El login valida el formato de la contraseña

**Qué pasa.** `LoginRequest.password` tiene `min_length=8`.

**Qué implica.** Una contraseña de siete caracteres recibe `422` en vez de `401`, lo
que le confirma a quien lo intenta que el formato importa. Y deja fuera a cualquier
usuario creado antes de esa regla.

**Qué haría falta.** Quitar la restricción. En el login no se valida el formato de la
credencial, se verifica si es correcta.

### 9. `CommentUpdate` no exige longitud mínima

**Qué pasa.** `CommentCreate.content` exige 10 caracteres; `CommentUpdate.content` no
exige nada.

**Qué implica.** Un comentario nace con al menos 10 caracteres y se puede editar a
uno. La regla solo se aplica en la mitad de los casos.

**Qué haría falta.** La misma restricción en los dos esquemas.

---

## Deuda técnica

### 10. `datetime.utcnow()` está deprecado

**Qué pasa.** `core/security.py` lo usa para calcular la expiración del token.

**Qué implica.** Aviso de deprecación desde Python 3.12, y devuelve un `datetime` sin
zona horaria, que es la causa habitual de errores al comparar fechas.

**Qué haría falta.** `datetime.now(timezone.utc)`.

---

## Pendientes de alcance

No son defectos: son cosas que el proyecto todavía no hace.

| | Qué implica |
|---|---|
| **Paginación** | `GET /tasks/`, `GET /users/` y `GET /comment/` devuelven todo. Con muchos registros la respuesta pesa demasiado |
| **Filtros por parámetros de consulta** | La visibilidad ya filtra por rol, pero el cliente no puede afinar por estado, proyecto o asignado |
| **Capa de repositorio** | Los servicios consultan el ORM directamente y lanzan `HTTPException`, así que están acoplados a HTTP |
| **Async** | Todo es sincrónico. Con SQLAlchemy síncrono es la decisión correcta, pero limita la concurrencia |
| **Cobertura de pruebas** | Hay pruebas de autenticación y usuarios. Faltan proyectos, tareas, comentarios y los permisos por rol |
| **Docker y despliegue** | Hoy solo corre en local |
| **Refresh tokens** | La sesión dura lo que dure el access token |
