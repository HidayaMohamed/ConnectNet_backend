from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database import get_db
from models import Like, User, Post

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/{user_id}/{post_id}", status_code=status.HTTP_201_CREATED)
def like_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not db.query(Post).filter(Post.id == post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing_like = db.query(Like).filter(and_(
        Like.user_id == user_id,
        Like.post_id == post_id
    )).first()

    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked")

    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()
    db.refresh(like)

    return {"id": like.id, "user_id": like.user_id, "post_id": like.post_id, "message": "Liked"}

@router.delete("/{user_id}/{post_id}")
def unlike_post(user_id: int, post_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(and_(
        Like.user_id == user_id,
        Like.post_id == post_id
    )).first()

    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")

    db.delete(like)
    db.commit()

    return {"message": "Unliked"}

@router.get("/post/{post_id}")
def get_likes(post_id: int, db: Session = Depends(get_db)):
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"post_id": post_id, "likes": count}