from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from app.db.deps import get_db
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials 
    try: 
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid token")
    
    return user

def require_role(required_role: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.rol.value not in required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied: requires {required_role} role"
            )
        return current_user
    return role_checker


