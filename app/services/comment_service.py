from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment
from app.models.user import User


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
    

def update_comment( db: Session, comment_id: int, data:CommentUpdate, current_user: User) -> Comment:
    comment = get_comment(db, comment_id)
    
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments"
        )
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment( db: Session, comment_id: int, current_user: User) -> None:
    comment = get_comment(db, comment_id)
    
    if comment.user_id != current_user.id and current_user.rol.value != "ADMIN":
        raise HTTPException(
        status_code=403,
        detail="You can only delete your own comments"
    )
    
    db.delete(comment)
    db.commit()