# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext # For hashing the password

from database import get_db
from models import User, Post, Follow
from schemas import UserCreate # Corrected import

router = APIRouter(prefix="/users", tags=["Users"])

# Define hasher here to ensure it's available for creating users
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Endpoint to create a new user (Registration)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first() or \
       db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # CRITICAL: HASH THE PASSWORD
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

# ... (Paste your existing get_users and get_user endpoints below here)