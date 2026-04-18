from fastapi import APIRouter
from app.schemas.users import UserCreate

# APIRouter es como un mini-FastAPI
# agrupa endpoints relacionados bajo un mismo recurso
router = APIRouter()

@router.get("/")
def get_users():
    # Por ahora retornamos datos falsos
    # En el Tema 5 conectamos con la base de datos real
    return [
        {"id": 1, "name": "Fernando", "role": "ADMIN"},
        {"id": 2, "name": "Carlos",   "role": "DEVELOPER"},
    ]

@router.get("/{user_id}")
def get_user(user_id: int):
    # {user_id} es un path parameter
    # FastAPI lo captura automáticamente y lo pasa a la función
    # el tipo int valida que sea un número — si mandás letras, error 422
    return {"id": user_id, "name": "Fernando", "role": "ADMIN"}

@router.post("/")
def create_user(user: UserCreate):
    return{
        "message": "Usuario creado exitosamente",
        "user": user
    }