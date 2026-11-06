from pydantic import BaseModel, EmailStr, Field, field_validator

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    
    @field_validator("email")
    @classmethod
    def normalizar_email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().lower()
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str