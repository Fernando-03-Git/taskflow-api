from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(str, Enum):
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    status: TaskStatus
    assigned_to: int
    project_id: int
    created_by: int
    
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
    status: Optional[TaskStatus] = None
    assigned_to: Optional[int] = None

