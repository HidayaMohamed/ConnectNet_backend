
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from pydantic import BaseModel

router = APIRouter()

class CommentCreate(BaseModel):
    user_id: int
    post_id: int
    content: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # check if user exists
    user = db.query(models.User).filter(models.User.id == comment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # check if post exists
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = models.Comment(
        user_id=comment.user_id,
        post_id=comment.post_id,
        content=comment.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"id": new_comment.id, "content": new_comment.content}
