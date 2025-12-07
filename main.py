from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import User, Post
from sqlalchemy.orm import Session
from database import get_db
# Import routers
from routers import users, auth, posts, comments, likes, follows

# Create FastAPI application
app = FastAPI(title="ConnectNet")

# Allowed frontend URLs
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(follows.router)

# Root endpoint
@app.get("/")
def root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    posts = db.query(Post).all()
    
    return {
        
        "users": [{"id": u.id, "username": u.username} for u in users],
        "posts": [{"id": p.id, "caption": p.caption} for p in posts]
    }