from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.core.enums import ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    description: str = Field(min_length=10, max_length=500)
    manager_id: int
    status: ProjectStatus = ProjectStatus.PENDING
    
class ProjectResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str
    status: ProjectStatus
    manager_id: int
    created_at: datetime
    created_by: int
    
class ProjectUpdate(BaseModel):
    
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    