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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

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