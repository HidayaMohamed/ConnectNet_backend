from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routers import auth, users, posts, comments, likes, follows

app = FastAPI(title= "ConnectNet")

# Allow your React frontend to talk to FastAPI
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
    
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(follows.router)

# Model for login
class LoginData(BaseModel):
    username: str
    password: str

# Fake "database" for now
USERS = {
    "admin": {"id": 1, "username": "admin", "password": "123"}
}

# Login route
@app.post("/auth/login")
async def login(data: LoginData):
    user = USERS.get(data.username)
    if user and user["password"] == data.password:
        return {
        "id": hash(data.username) % 10000,  # fake unique ID
        "username": data.username,
        "token": "fake-jwt-token"
    }
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Example "posts" route so you can post after logging in
POSTS = []

@app.post("/posts")
async def create_post(post: dict):
    POSTS.append(post)
    return post

@app.get("/posts")
async def get_posts():
    return POSTS
