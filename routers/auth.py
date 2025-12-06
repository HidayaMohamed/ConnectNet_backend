from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models import User
from schemas.auth import LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar
    }
