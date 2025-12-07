from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def root():
    return {"message": "ConnectNet API is running"}
