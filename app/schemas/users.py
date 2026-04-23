from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRol(str, Enum):
    admin     = "ADMIN"
    manager   = "MANAGER"
    developer = "DEVELOPER"

class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    rol: UserRol
    
class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    last_name: str
    email: str
    rol: UserRol
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None