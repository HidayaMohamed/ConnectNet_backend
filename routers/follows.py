from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from database import get_db
from models import Follow, User

router = APIRouter(prefix="/follows", tags=["Follows"])



@router.post("/{follower_id}/{following_id}", status_code=status.HTTP_201_CREATED)
def follow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    if follower_id == following_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot follow yourself")

    if not db.query(User).filter(User.id == follower_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follower not found")

    if not db.query(User).filter(User.id == following_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to follow not found")

    existing = db.query(Follow).filter(and_(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id
    )).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already following")

    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.add(follow)
    db.commit()
    db.refresh(follow)
    return {"id": follow.id, "follower_id": follow.follower_id, "following_id": follow.following_id, "message": "Now following"}

@router.delete("/{follower_id}/{following_id}")
def unfollow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    follow = db.query(Follow).filter(and_(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id
    )).first()

    if not follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Follow relationship not found")

    db.delete(follow)
    db.commit()

    return {"message": "Unfollowed"}

@router.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    followers = db.query(Follow).filter(Follow.following_id == user_id).all()
    return [{"id": f.id, "follower_id": f.follower_id, "following_id": f.following_id} for f in followers]

@router.get("/following/{user_id}")
def get_following(user_id: int, db: Session = Depends(get_db)):
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    return [{"id": f.id, "follower_id": f.follower_id, "following_id": f.following_id} for f in following]