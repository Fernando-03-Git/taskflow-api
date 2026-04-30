from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.task import TaskCreate,TaskResponse, TaskUpdate
from app.services import task_service
from app.core.dependencies import require_role, get_current_user

router = APIRouter()

@router.get("/", response_model= list[TaskResponse], dependencies= [Depends(get_current_user)])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@router.get("/{task_id}", response_model= TaskResponse, dependencies= [Depends(get_current_user)])
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)

@router.post("/", response_model= TaskResponse, status_code=201, dependencies= [Depends(require_role(["ADMIN", "MANAGER"]))])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # task ya llegó validado por Pydantic
    # si faltó algún campo o tiene tipo incorrecto
    # FastAPI lanzó 422 antes de llegar aquí
    return task_service.create_task(db, task)

@router.patch("/{task_id}", response_model=TaskResponse, dependencies= [Depends(get_current_user)])
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.update_task(db, task_id, data)