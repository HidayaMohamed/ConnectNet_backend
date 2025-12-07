from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Comment, User, Post

router = APIRouter(prefix="/comments", tags=["Comments"])

class CommentCreate(BaseModel):
    user_id: int
    post_id: int
    content: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == comment.user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not db.query(Post).filter(Post.id == comment.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = Comment(
        user_id=comment.user_id,
        post_id=comment.post_id,
        content=comment.content,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "id": new_comment.id,
        "user_id": new_comment.user_id,
        "post_id": new_comment.post_id,
        "content": new_comment.content,
    }

@router.get("/post/{post_id}")
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return [
        {
            "id": c.id,
            "user_id": c.user_id,
            "post_id": c.post_id,
            "content": c.content,
        }
        for c in comments
    ]