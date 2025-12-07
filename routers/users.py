from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import User, Post, Follow
from schemas.auth import UserCreate
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])

# Fetch all users
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).options(
        joinedload(User.posts),           # load user's posts
        joinedload(User.followers),       # load followers
        joinedload(User.following)        # load following
    ).all()

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "bio": user.bio,
            "avatar": user.avatar,
            "posts": [
                {
                    "id": post.id,
                    "caption": post.caption,
                    "media_url": post.media_url,
                    "media_type": post.media_type,
                    "created_at": post.created_at
                } for post in user.posts
            ],
            "followers": [f.follower_id for f in user.followers],
            "following": [f.following_id for f in user.following]
        })
    return result

# Fetch a single user by ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).options(
        joinedload(User.posts),
        joinedload(User.followers),
        joinedload(User.following)
    ).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar,
        "posts": [
            {
                "id": post.id,
                "caption": post.caption,
                "media_url": post.media_url,
                "media_type": post.media_type,
                "created_at": post.created_at
            } for post in user.posts
        ],
        "followers": [f.follower_id for f in user.followers],
        "following": [f.following_id for f in user.following]
    }
@router.post("/", status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    if db.query(User).filter(User.username == user_data.username).first() or \
       db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # **CRITICAL: HASH THE PASSWORD**
    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        bio=user_data.bio,
        avatar=user_data.avatar
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user