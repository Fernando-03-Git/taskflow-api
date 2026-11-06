from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from app.core.enums import Rol


class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    rol: Rol
    
    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str | None) -> str | None:
        if v is None: 
            return v
        return v.strip().lower()

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    
    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().lower()
    
class UserUpdatePassword(BaseModel):
    password_current: str 
    password_new: str = Field(min_length=8)
    
class UserResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    last_name: str
    email: str
    rol: Rol
    is_active: bool
    created_at: datetime

