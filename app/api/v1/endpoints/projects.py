from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services  import project_service
from app.schemas.projects import ProjectCreate, ProjectResponse, ProjectUpdate
from app.core.dependencies import require_role, get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model= list[ProjectResponse], dependencies= [Depends(get_current_user)])
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_projects(db)

@router.get("/{project_id}", response_model= ProjectResponse, dependencies= [Depends(get_current_user)])
def get_project(project_id: int, db: Session = Depends(get_db)):
    return project_service.get_project(db, project_id)

@router.post("/", response_model= ProjectResponse, status_code=201, dependencies= [Depends(require_role(["ADMIN", "MANAGER"]))])
def create_project(project: ProjectCreate,current_user: User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    return project_service.create_project(db, project, current_user.id)

@router.patch("/{project_id}", response_model= ProjectResponse, dependencies= [Depends(require_role(["ADMIN", "MANAGER"]))])
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    return project_service.update_project(db, project_id, data)