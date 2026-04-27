from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate

def get_project(db: Session, project_id: int) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=404,
            detail=f"Project with id {project_id} not found"
        )
        
    return project

def get_projects(db: Session) ->list[Project]:
    return db.query(Project).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(**project.model_dump())
    
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

