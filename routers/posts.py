
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from pydantic import BaseModel

router = APIRouter()

class PostCreate(BaseModel):
    user_id: int
    caption: str = None
    media_url: str = None
    media_type: str = None

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # check if user exists
    user = db.query(models.User).filter(models.User.id == post.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_post = models.Post(
        user_id=post.user_id,
        caption=post.caption,
        media_url=post.media_url,
        media_type=post.media_type
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"id": new_post.id, "caption": new_post.caption, "user_id": new_post.user_id}

@router.get("/")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
