from sqlalchemy.orm import Session
from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment

def get_comments(db: Session) -> list[Comment]:
    return db.query(Comment).all()

def get_comment(db:Session, comment_id: int) -> Comment:
    return db.query(Comment).filter(Comment.id == comment_id).first()

def create_comment(db: Session, comment: CommentCreate) -> Comment:
    db_comment = Comment(
        content = comment.content,
        task_id = comment.task_id,
        user_id = comment.user_id
    )
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