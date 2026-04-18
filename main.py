from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title= settings.app_name,
    description="Sistema de gestión de tareas y proyectos colaborativos",
    version= settings.app_version
)

# Registramos el router principal
# prefix /api/v1 → todas las rutas empiezan con /api/
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
        }
