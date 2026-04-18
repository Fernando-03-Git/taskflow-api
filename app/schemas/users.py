from pydantic import BaseModel, Field, EmailStr
from enum import Enum

class UserRol(str, Enum):
    admin     = "ADMIN"
    manager   = "MANAGER"
    developer = "DEVELOPER"

class UserCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str = Field(min_length=8)
    rol: UserRol