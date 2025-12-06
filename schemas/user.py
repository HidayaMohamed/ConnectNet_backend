from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    name: str  = None
    bio: str  = None
    avatar: str = None

class UserUpdate(BaseModel):
    username: str  = None
    name: str  = None
    bio: str  = None
    avatar: str = None