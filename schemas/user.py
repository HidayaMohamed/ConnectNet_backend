from pydantic import BaseModel

# Schema used when creating a user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    name: str = None
    bio: str = None
    avatar: str = None

# Schema used when updating a user
class UserUpdate(BaseModel):
    username: str = None
    name: str = None
    bio: str = None
    avatar: str = None
