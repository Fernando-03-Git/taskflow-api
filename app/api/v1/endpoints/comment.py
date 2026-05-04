from fastapi import APIRouter, Depends
from app.db.deps import get_db
from app.services import comment_service
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.core.dependencies import get_current_user, require_role
from app.models.user import User

router = APIRouter()

@router.get("/", response_model= list[CommentResponse], dependencies= [Depends(get_current_user)])
def get_comments(db: Session = Depends(get_db)):
    return comment_service.get_comments(db)

@router.get("/{comment_id}", response_model= CommentResponse, dependencies= [Depends(get_current_user)])
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comment(db, comment_id)

@router.post("/", response_model=CommentResponse, status_code=201)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return comment_service.create_comment(db, comment, current_user.id)

@router.patch("/{comment_id}", response_model= CommentResponse, dependencies= [Depends(get_current_user)])
def update_comment(comment_id: int, data: CommentUpdate, db: Session = Depends(get_db)):
    return comment_service.update_comment(db, comment_id, data)

@router.delete("/{comment_id}", status_code=204, dependencies= [Depends(require_role(["ADMIN"]))])
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_service.delete_comment(db, comment_id)