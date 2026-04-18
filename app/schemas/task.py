from pydantic import BaseModel, Field
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    review      = "review"
    done        = "done"

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    status: TaskStatus
    assigned_to: str

