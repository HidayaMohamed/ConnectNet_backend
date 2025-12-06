from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    name: str | None = None
    bio: str | None = None
    avatar: str | None = None

class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    bio: str | None = None
    avatar: str | None = None