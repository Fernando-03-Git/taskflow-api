# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The project uses a local venv at `venv/` (Windows). Activate it first: `venv\Scripts\activate`.

```powershell
uvicorn main:app --reload          # dev server on http://localhost:8000 (docs at /docs)
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
pytest                             # all tests
pytest app/tests/test_auth.py      # one file
pytest app/tests/test_auth.py::test_login_success   # one test
pytest -v -s                       # verbose + see print() from the logging middleware
```

There is no linter/formatter configured.

### Testing setup

`app/tests/conftest.py` derives the test DB URL from `DATABASE_URL` by string-replacing `taskflow` → `taskflow_test`, so a **`taskflow_test` database must already exist in Postgres** (tables are created/dropped per session by the `setup_database` fixture, but the database itself is not). If the dev DB is named something else, that replacement silently does nothing and tests will run against the real DB.

Fixtures: `db` (session), `client` (TestClient with `get_db` overridden), `test_user` (ADMIN user, password `123456789`), `admin_token` (JWT string — pass as `headers={"Authorization": f"Bearer {token}"}`).

`requirements.txt` is UTF-16 encoded and does **not** list `pytest`/`httpx`, which are installed in the venv only. Re-generating it with `pip freeze` will change encoding and add those.

## Architecture

FastAPI + SQLAlchemy 2.0 (typed `Mapped[]` models) + Alembic + Pydantic v2, PostgreSQL. Layered, with one module per resource at each layer:

```
main.py                        app setup: CORS, logging/security-headers middleware, global exception handlers
app/api/v1/router.py           mounts the five endpoint routers; main.py mounts it at /api/v1
app/api/v1/endpoints/*.py      routing + auth dependencies only; delegate to services
app/services/*.py              business logic; the only place HTTPException is raised for domain errors
app/schemas/*.py               Pydantic request/response models
app/models/*.py                SQLAlchemy models (Base lives in app/db/session.py)
app/core/                      config (settings), security (hashing/JWT), dependencies (auth)
```

Endpoints stay thin: they resolve dependencies and call a service function, passing `db` plus (where relevant) `current_user.id`. Services do queries, raise `HTTPException` for not-found/conflict, and commit.

### Auth

- `POST /api/v1/auth/` takes `{email, password}` (not an OAuth2 form) and returns `{access_token, token_type}`.
- The JWT payload is `{"sub": str(user.id), "rol": <ROL value>, "exp": ...}`. `get_current_user` reads only `sub` and re-queries the user; the `rol` claim is informational.
- Transport is `HTTPBearer` (not `OAuth2PasswordBearer`) — chosen so Swagger's Authorize accepts a raw token.
- `require_role([...])` in `app/core/dependencies.py` is a dependency factory checking `current_user.rol.value`. It expects a **list**; `app/api/v1/endpoints/users.py` currently passes the bare string `"ADMIN"`, which only works because `in` falls back to substring matching. Pass lists in new code.
- Ownership fields (`created_by` on tasks/projects, `user_id` on comments) are never accepted from the request body — the endpoint injects `current_user.id` into the service call, and the `*Create` schemas deliberately omit them.

### Enums and migrations

`Rol` and `Status` use identical uppercase name and value (`ADMIN = "ADMIN"`), because SQLAlchemy persists the enum *name* while Pydantic serializes the *value*; keeping them equal is what makes both directions agree. Preserve that pattern when adding enum members. Note that `Project.status` and `Task.status` share the Postgres enum type name `status`.

`alembic/env.py` overrides `sqlalchemy.url` from `settings.database_url` at runtime, so the placeholder in `alembic.ini` is unused. It also imports `app.models` explicitly — new models must be re-exported from `app/models/__init__.py` or autogenerate will miss them.

### Error responses

Both handlers in `main.py` return a uniform body: `{"error": true, "status_code": N, "detail": ...}`. Unhandled exceptions always become a generic 500 with no detail leaked. Tests and clients should expect this shape, not FastAPI's default `{"detail": ...}`.

## Conventions

Comments, commit messages and the README are in Spanish; user-facing API `detail` strings are in English. Commits follow `tipo: descripción` (`feat:`, `fix:`, `refactor:`) written in first person past tense.

`readme.md` is out of date — it still says the project has no authentication.
