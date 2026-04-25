from pydantic import Field, BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str = Field(min_length=10, max_length=200)
    task_id: int
    user_id: int

class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    content: str
    task_id: int
    user_id: int
    created_at: datetime
    
class CommentUpdate(BaseModel):
    content: Optional[str] = None
    