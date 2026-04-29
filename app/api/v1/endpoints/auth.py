from fastapi import Depends, APIRouter
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_user
from app.db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model= TokenResponse)
def user_auth(user: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, user.email, user.password)