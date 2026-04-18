from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    nombre: str
    descripcion: str = Field(min_length=10, max_length=500)
    creado_by: int