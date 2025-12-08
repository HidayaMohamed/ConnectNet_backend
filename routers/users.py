# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext 

from database import get_db
from models import User, Post, Follow
from schemas import UserCreate 

router = APIRouter(prefix="/users", tags=["Users"])


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")



@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first() or \
       db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    
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
    
    return {"id": new_user.id, "username": new_user.username}

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }