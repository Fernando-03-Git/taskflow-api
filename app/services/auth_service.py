from app.core.security import create_access_token, verify_password
from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException

def authenticate_user(db: Session, email:str, password:str) -> dict:
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid credentials"
        )
    
    password_verify = verify_password(password, user.password)
    
    if not password_verify:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid credentials"
        )
    
    data: dict = {
        "sub": str(user.id),
        "rol": user.rol.value
    }
    
    return {
        "access_token": create_access_token(data),
        "token_type": "bearer"
    }