from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.core.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    assigned_to: int
    project_id: int
    
class TaskResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    status: TaskStatus
    project_id: int
    assigned_to: int
    created_by: int
    created_at: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskUpdateStatus(BaseModel):
    status: TaskStatus

class TaskUpdateAssigneeTo(BaseModel):
    assigned_to: int
