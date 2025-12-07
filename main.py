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

@app.get("/")
def root():
    return {"message": "ConnectNet API is running."}