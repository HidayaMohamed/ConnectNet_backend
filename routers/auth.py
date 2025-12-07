# FastAPI tools
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Password hashing library
from passlib.context import CryptContext

# Local imports
from database import get_db
from models import User
from schemas.auth import LoginRequest

# Create router object
router = APIRouter(prefix="/auth", tags=["Auth"])

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    # Get user by username
    user = db.query(User).filter(User.username == credentials.username).first()

    # If no user or wrong password
    if not user or not pwd_context.verify(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Return user data
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "name": user.name,
        "bio": user.bio,
        "avatar": user.avatar,
    }
