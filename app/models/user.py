from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy import String, DateTime, func

class Rol(enum.Enum):
    ADMIN     = "ADMIN"
    MANAGER   = "MANAGER"
    DEVELOPER = "DEVELOPER"

class User(Base):
    __tablename__= "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(String(60))
    rol: Mapped[Rol] = mapped_column(Enum(Rol))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )