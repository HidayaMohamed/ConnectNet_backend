
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from database import get_db
from models import Like, User, Post
from pydantic import BaseModel
 

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/{user_id}/{post_id}")
def like_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    # Check user and post
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(404, "User not found")
    if not db.query(Post).filter(Post.id == post_id).first():
        raise HTTPException(404, "Post not found")

    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()

    if existing_like:
        raise HTTPException(400, "Already liked")

    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()
    return {"message": "Liked"}

@router.delete("/{user_id}/{post_id}")
def unlike_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()

    if not like:
        raise HTTPException(404, "Like not found")

    db.delete(like)
    db.commit()
    return {"message": "Unliked"}

@router.get("/post/{post_id}")
def get_likes(post_id: int, db: Session = Depends(get_db)):
    return db.query(Like).filter(Like.post_id == post_id).count()