from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import Enum
from datetime import datetime
from sqlalchemy import String, func, DateTime
from app.core.enums import TaskStatus



class Task(Base):
    __tablename__= "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(500))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    