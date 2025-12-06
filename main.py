
from fastapi import FastAPI
from .routers import users,posts, comments, likes, follows

app = FastAPI(title="ConnectNet")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comments.router, prefix="/comments", tags=["Comments"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])
app.include_router(follows.router, prefix="/follows", tags=["Follows"])

@app.get("/")
def root():
    return {"message": "ConnectNet API is running"}
