# schemas.py
from pydantic import BaseModel

# AUTH
class LoginRequest(BaseModel):
    username: str
    password: str

# USERS 
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    name: str = None
    bio: str = None
    avatar: str = None

# POSTS 
class PostCreate(BaseModel):
    user_id: int 
    caption: str
    media_url: str = None
    media_type: str = None

    class Config:
        orm_mode = True