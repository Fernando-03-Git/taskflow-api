from fastapi import APIRouter
from app.api.v1.endpoints import users, projects, tasks, comment, auth

# Router principal que agrupa todos los routers
api_router = APIRouter()

# Registramos el router de usuarios
# prefix  → todas las rutas de users tendrán /users al inicio
# tags    → agrupa los endpoints en Swagger UI
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

api_router.include_router(
    projects.router,
    prefix= "/projects",
    tags=["Projects"]
    
)

api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"]
)

api_router.include_router(
    comment.router,
    prefix="/comment",
    tags=["Comment"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)