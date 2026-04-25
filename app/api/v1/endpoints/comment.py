from fastapi import APIRouter, Depends
from app.db.deps import get_db
from app.services import comment_service
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter()

@router.get("/", response_model= list[CommentResponse])
def get_comments(db: Session = Depends(get_db)):
    return comment_service.get_comments(db)

@router.get("/{comment_id}", response_model= CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comment(db, comment_id)

@router.post("/", response_model= CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return comment_service.create_comment(db, comment)

@router.patch("/{comment_id}", response_model= CommentResponse)
def update_comment(comment_id: int, data: CommentUpdate, db: Session = Depends(get_db)):
    return comment_service.update_comment(db, comment_id, data)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.delete_comment(db, comment_id)