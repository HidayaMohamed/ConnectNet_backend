from pydantic import BaseModel

# Schema for login request
class LoginRequest(BaseModel):
    username: str
    password: str
