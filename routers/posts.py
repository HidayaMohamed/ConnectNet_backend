from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import models

router = APIRouter(prefix="/posts", tags=["Posts"])

# Schema for creating posts
class PostCreate(BaseModel):
    user_id: int
    caption: str = None
    media_url: str = None
    media_type: str = None

@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == post.user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Create post object
    new_post = models.Post(
        user_id=post.user_id,
        caption=post.caption,
        media_url=post.media_url,
        media_type=post.media_type
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Return important fields
    return {
        "id": new_post.id,
        "caption": new_post.caption,
        "user_id": new_post.user_id
    }

@router.get("/")
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
