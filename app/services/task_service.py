from sqlalchemy.orm import Session
from app.models.task import Task, Status
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()

def get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(task_id == Task.id).first()

def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(
        title = task.title,
        description = task.description,
        status = Status.PENDING,
        project_id = task.project_id,
        assigned_to = task.assigned_to,
        created_by = task.created_by
    )
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
        