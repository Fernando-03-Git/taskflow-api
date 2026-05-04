from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()

def get_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found"
        )
    
    return task

def create_task(db: Session, task: TaskCreate, created_by: int) -> Task:
    
    task_data = task.model_dump()
    task_data["created_by"] = created_by
    
    db_task = Task(**task_data)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, data: TaskUpdate) -> Task:
    task = get_task(db, task_id)
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task
        