from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate
from sqlalchemy.orm import Session

def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session) -> list[User]:
    return db.query(User).all()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        name = user.name,
        last_name = user.last_name,
        email = user.email,
        password = user.password,
        rol = user.rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user(db, user_id)
    for key, value in data.model_dump(exclude_unset= True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int) -> User:
    user = get_user(db, user_id)
    user.is_active = False
    db.commit()
    return user