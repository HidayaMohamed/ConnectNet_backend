
from fastapi import FastAPI
from .routers import users, auth, posts, comments, likes, follows

app = FastAPI(title="ConnectNet")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(follows.router)

@app.get("/")
def root():
    return {"message": "ConnectNet API is running"}
