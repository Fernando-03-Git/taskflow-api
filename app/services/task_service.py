from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskUpdateStatus
from app.core.enums import TaskStatus, Rol
from app.services.project_service import get_project
from app.services.user_service import get_user

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

def create_task(db: Session, task: TaskCreate, current_user: User) -> Task:
    project = get_project(db, task.project_id)
    assignee = get_user(db, task.assigned_to)
    
    if project.manager_id != current_user.id and current_user.rol != Rol.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only the project manager or an ADMIN can create tasks in this project"
        )
    
    if not assignee.is_active:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {task.assigned_to} is deactivated and cannot be assigned tasks"
        )
    
    task_data = task.model_dump()
    task_data["created_by"] = current_user.id
    
    db_task = Task(**task_data)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, data: TaskUpdate, current_user: User) -> Task:
    task = get_task(db, task_id)
    
    project = get_project(db, task.project_id)
    
    if task.created_by != current_user.id and current_user.rol != Rol.ADMIN and current_user.id != project.manager_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to edit this task"
        )
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, data: TaskUpdateStatus, current_user: User) -> Task:
    task = get_task(db, task_id)
    project = get_project(db, task.project_id)
    current_status = task.status
    new_status = data.status
    
    if (current_status == TaskStatus.PENDING and new_status == TaskStatus.COMPLETED) or (current_status == TaskStatus.COMPLETED and new_status == TaskStatus.PENDING):
        raise HTTPException(
            status_code=409,
            detail="status action is not allowed"
        )
        
    if current_status == new_status:
        raise HTTPException(
            status_code=409,
            detail="there is nothing to change"
        )
    
    if (current_status == TaskStatus.PENDING and new_status == TaskStatus.IN_PROGRESS or current_status == TaskStatus.IN_PROGRESS and new_status == TaskStatus.PENDING) and (task.assigned_to != current_user.id and project.manager_id != current_user.id and current_user.rol != Rol.ADMIN) :
        raise HTTPException(
            status_code=403,
            detail="solo el asignado, el manager o un admin"
        )
    
    if (current_status == TaskStatus.COMPLETED and new_status == TaskStatus.IN_PROGRESS or current_status == TaskStatus.IN_PROGRESS and new_status == TaskStatus.COMPLETED) and (project.manager_id != current_user.id and current_user.rol != Rol.ADMIN) :
        raise HTTPException(
            status_code=403,
            detail="solo el manager del proyecto o un admin pueden completar"
            )
        
    task.status = new_status
    db.commit()
    db.refresh(task)
    return task