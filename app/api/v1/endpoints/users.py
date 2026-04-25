from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services import user_service
from app.schemas.users import UserCreate, UserResponse, UserUpdate

# APIRouter es como un mini-FastAPI
# agrupa endpoints relacionados bajo un mismo recurso
router = APIRouter()

@router.get("/", response_model= list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/{user_id}", response_model= UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # {user_id} es un path parameter
    # FastAPI lo captura automáticamente y lo pasa a la función
    # el tipo int valida que sea un número — si mandás letras, error 422
    return user_service.get_user(db, user_id)

@router.post("/", response_model= UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.delete("/{user_id}")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.deactivate_user(db, user_id)

@router.patch("/{user_id}", response_model= UserResponse)
def update_user(data: UserUpdate, user_id: int, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)