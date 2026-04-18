from fastapi import APIRouter
from app.schemas.task import TaskCreate

router = APIRouter()

@router.get("/")
def get_tasks():
    return[
        {
            "id": 1,
            "title": "hacer endpoints",
            "status": "pendiente",
            "assigned_to": "Fernando"
        },
        
        {
            "id": 2,
            "tittle": "crear ladingpage",
            "status": "pendiente",
            "assined_to": "Marifer"
        }
    ]

@router.get("/{task_id}")
def get_task(task_id: int):
    return{
        "id": task_id,
        "title": "crear ladingpage",
        "status": "pendiente",
        "assigned_to": "Marifer"
    }

@router.post("/")
def create_task(task: TaskCreate):
    # task ya llegó validado por Pydantic
    # si faltó algún campo o tiene tipo incorrecto
    # FastAPI lanzó 422 antes de llegar aquí
    return{
        "message": "Tarea creada exitosamente",
        "task": task
    }