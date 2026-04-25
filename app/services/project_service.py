from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate
from app.models.project import Status

def get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).filter(project_id == Project.id).first()

def get_projects(db: Session) ->list[Project]:
    return db.query(Project).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(
        name = project.name,
        description = project.description,
        manager_id = project.manager_id,
        created_by = project.created_by,
        status = Status.PENDING
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project_id: int, data: ProjectUpdate) -> Project:
    project = get_project(db, project_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

