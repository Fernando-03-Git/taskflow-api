from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import enum
from datetime import datetime

class Status(str, enum.Enum):
    PENDING     = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"


class ProjectCreate(BaseModel):
    name: str
    description: str = Field(min_length=10, max_length=500)
    manager_id: int
    status: Status = Status.PENDING
    
class ProjectResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str
    status: Status
    manager_id: int
    created_at: datetime
    created_by: int
    
class ProjectUpdate(BaseModel):
    
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    