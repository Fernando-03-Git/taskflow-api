from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services  import project_service
from app.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()

@router.get("/", response_model= list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_projects(db)

@router.get("/{project_id}", response_model= ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return project_service.get_project(db, project_id)

@router.post("/", response_model= ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return project_service.create_project(db, project)

@router.patch("/{project_id}", response_model= ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    return project_service.update_project(db, project_id, data)