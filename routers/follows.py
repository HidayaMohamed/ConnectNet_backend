
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database
from pydantic import BaseModel

router = APIRouter()

class FollowCreate(BaseModel):
    follower_user_id: int
    following_user_id: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def follow_user(follow: FollowCreate, db: Session = Depends(get_db)):
    if follow.follower_user_id == follow.following_user_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    existing_follow = db.query(models.Follow).filter(
        models.Follow.follower_user_id == follow.follower_user_id,
        models.Follow.following_user_id == follow.following_user_id
    ).first()
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following")
    
    new_follow = models.Follow(
        follower_user_id=follow.follower_user_id,
        following_user_id=follow.following_user_id
    )
    db.add(new_follow)
    db.commit()
    return {"status": "following"}

@router.delete("/")
def unfollow_user(follow: FollowCreate, db: Session = Depends(get_db)):
    existing_follow = db.query(models.Follow).filter(
        models.Follow.follower_user_id == follow.follower_user_id,
        models.Follow.following_user_id == follow.following_user_id
    ).first()
    if not existing_follow:
        raise HTTPException(status_code=404, detail="Follow not found")
    
    db.delete(existing_follow)
    db.commit()
    return {"status": "unfollowed"}
