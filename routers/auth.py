from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

# Use the working pbkdf2_sha256 algorithm
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()

    # Verify password 
    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Return user data 
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar,
    }