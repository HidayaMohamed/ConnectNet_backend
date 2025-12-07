from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas.user import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username/email already exists
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing:
        raise HTTPException(400, "Username or Email already exists")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create user object
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        name=user.name,
        bio=user.bio,
        avatar=user.avatar,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(404, "User not found")

    return user

@router.put("/{id}")
def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Update only fields provided
    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user
