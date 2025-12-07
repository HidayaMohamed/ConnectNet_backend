from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Follow, User

router = APIRouter(prefix="/follows", tags=["Follows"])

@router.post("/{follower_id}/{following_id}")
def follow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    # Prevent self-follow
    if follower_id == following_id:
        raise HTTPException(400, "You cannot follow yourself")

    # Checks if both users exist
    if not db.query(User).filter(User.id == follower_id).first():
        raise HTTPException(404, "Follower not found")

    if not db.query(User).filter(User.id == following_id).first():
        raise HTTPException(404, "User to follow not found")

    # Checks if lready following
    existing = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id
    ).first()

    if existing:
        raise HTTPException(400, "Already following")

    # Create follow entry
    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )

    db.add(follow)
    db.commit()

    return {"message": "Now following"}

@router.delete("/{follower_id}/{following_id}")
def unfollow_user(follower_id: int, following_id: int, db: Session = Depends(get_db)):
    follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id
    ).first()

    if not follow:
        raise HTTPException(404, "Follow relationship not found")

    db.delete(follow)
    db.commit()

    return {"message": "Unfollowed"}

@router.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    return db.query(Follow).filter(Follow.following_id == user_id).all()

@router.get("/following/{user_id}")
def get_following(user_id: int, db: Session = Depends(get_db)):
    return db.query(Follow).filter(Follow.follower_id == user_id).all()
