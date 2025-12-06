
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from pydantic import BaseModel
from ..database import get_db
from ..models import Comment, User, Post

router = APIRouter(prefix="/comments", tags=["Comments"])

class CommentCreate(BaseModel):
    user_id: int
    post_id: int
    content: str

@router.post("/")
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == comment.user_id).first():
        raise HTTPException(404, "User not found")

    if not db.query(Post).filter(Post.id == comment.post_id).first():
        raise HTTPException(404, "Post not found")

    new_comment = Comment(
        user_id=comment.user_id,
        post_id=comment.post_id,
        content=comment.content,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/post/{post_id}")
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.post_id == post_id).all()