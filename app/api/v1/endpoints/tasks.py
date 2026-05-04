from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.task import TaskCreate,TaskResponse, TaskUpdate
from app.services import task_service
from app.core.dependencies import require_role, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model= list[TaskResponse], dependencies= [Depends(get_current_user)])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@router.get("/{task_id}", response_model= TaskResponse, dependencies= [Depends(get_current_user)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["ADMIN", "MANAGER"]))
):
    return task_service.create_task(db, task, current_user.id)

@router.patch("/{task_id}", response_model=TaskResponse, dependencies= [Depends(get_current_user)])
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, data)