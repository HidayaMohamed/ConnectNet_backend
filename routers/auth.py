# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import LoginRequest # Corrected import from local schemas.py

router = APIRouter(prefix="/auth", tags=["Auth"])

# **CRITICAL FIX: Use the working pbkdf2_sha256 algorithm**
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()

    # Verify password using the new scheme
    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Return user data (you would normally return a JWT here)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar,
    }