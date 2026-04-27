from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title= settings.app_name,
    description="Sistema de gestión de tareas y proyectos colaborativos",
    version= settings.app_version
)

# ─── Manejador 1: errores HTTP intencionales ───────────────────────────────
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail
        }
    )

# ─── Manejador 2: errores inesperados del servidor ─────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "detail": "Internal server error"
        }
    )

# ─── Router principal ──────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
        }
