from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment

def get_comments(db: Session) -> list[Comment]:
    return db.query(Comment).all()

def get_comment(db:Session, comment_id: int) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=404,
            detail=f"Comment with id {comment_id} not found"
        )
    
    return comment

def create_comment(db: Session, comment: CommentCreate, user_id: int) -> Comment:
    
    comment_data = comment.model_dump()
    comment_data["user_id"] = user_id
    
    db_comment = Comment(**comment_data)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
    

def update_comment( db: Session, comment_id: int, data:CommentUpdate) -> Comment:
    comment = get_comment(db, comment_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment( db: Session, comment_id: int) -> None:
    comment = get_comment(db, comment_id)
    db.delete(comment)
    db.commit()