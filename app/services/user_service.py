from fastapi import HTTPException
from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate
from sqlalchemy.orm import Session
from app.core.security import hash_password

def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    
    return user

def get_users(db: Session) -> list[User]:
    return db.query(User).all()

def create_user(db: Session, user: UserCreate) -> User:
    
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail=f"Email {user.email} is already registered"
        )
        
    password_hash = hash_password(user.password) 
    
    user_data = user.model_dump()
    
    user_data["password"] = password_hash
    
    
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user(db, user_id)
    
    if data.email:
        existing_email = db.query(User).filter(
            User.email == data.email,
            User.id != user_id
            ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=409,
                detail=f"Email {data.email} is already registered"
            )
    
    for key, value in data.model_dump(exclude_unset= True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int) -> User:
    user = get_user(db, user_id)
    
    if user.is_active == False:
        raise HTTPException(
            status_code=409,
            detail=f"User {user.name} is already deactivated"
        )
    
    user.is_active = False
    db.commit()
    return user