from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
import enum
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy import String, func, DateTime

class Status(enum.Enum):
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"

class Task(Base):
    __tablename__= "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(500))
    status: Mapped[Status] = mapped_column(Enum(Status))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    