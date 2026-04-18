from fastapi import APIRouter
from app.schemas.projects import ProjectCreate

router = APIRouter()

@router.get("/")
def get_projects():
    return [
        {
            "id": 1,
            "name": "ScaryMovie"
        },
        {
            "id": 2,
            "name": "AmericaPie"
        }
    ]
@router.get("/{project_id}")
def get_project(project_id: int):
    return{
            "id": project_id,
            "name": "ScaryMovie "
        }
    
@router.post("/")
def create_project(project: ProjectCreate):
    return{
        "message": "Proyecto creado exitosamente",
        "project": project
    }