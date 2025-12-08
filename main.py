from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import User, Post, Comment, Like

from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.comments import router as comments_router
from routers.likes import router as likes_router
from routers.follows import router as follows_router
from routers.auth import router as auth_router

app = FastAPI(title="ConnectNet API")

# Allow React frontend to communicate with FastAPI
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

# Include all routers
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(follows_router)
app.include_router(auth_router)

# Example root endpoint
@app.get("/")
def root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    users_data = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "name": u.name,
            "bio": u.bio,
            "avatar": u.avatar,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in users
    ]

    posts = (
        db.query(Post)
        .options(
            joinedload(Post.user),
            joinedload(Post.comments).joinedload(Comment.user),
            joinedload(Post.likes).joinedload(Like.user),
        )
        .all()
    )

    posts_data = []
    for p in posts:
        post_user = {
            "id": p.user.id,
            "username": p.user.username,
            "name": p.user.name,
            "avatar": p.user.avatar,
        } if p.user else None

        comments = [
            {
                "id": c.id,
                "user_id": c.user_id,
                "content": c.content,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "user": {
                    "id": c.user.id,
                    "username": c.user.username,
                    "name": c.user.name,
                    "avatar": c.user.avatar,
                } if c.user else None,
            }
            for c in p.comments
        ]

        likes = [
            {
                "user_id": l.user_id,
                "created_at": l.created_at.isoformat() if l.created_at else None,
                "user": {
                    "id": l.user.id,
                    "username": l.user.username,
                    "name": l.user.name,
                    "avatar": l.user.avatar,
                } if l.user else None,
            }
            for l in p.likes
        ]

        posts_data.append({
            "id": p.id,
            "user_id": p.user_id,
            "caption": p.caption,
            "media_url": p.media_url,
            "media_type": p.media_type,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "user": post_user,
            "comments": comments,
            "likes": likes,
            "like_count": len(likes),
        })

    return {"users": users_data, "posts": posts_data}
