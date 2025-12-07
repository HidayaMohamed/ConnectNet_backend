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

# Allow your React frontend to talk to FastAPI
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
    
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(follows_router)
app.include_router(auth_router)


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
            "created_at": u.created_at.isoformat() if getattr(u, "created_at", None) else None,
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
        p_user = getattr(p, "user", None)
        post_user = {
            "id": getattr(p_user, "id", None),
            "username": getattr(p_user, "username", None),
            "name": getattr(p_user, "name", None),
            "avatar": getattr(p_user, "avatar", None),
        } if p_user else None

        comments = []
        for c in getattr(p, "comments", []) or []:
            c_user = getattr(c, "user", None)
            comments.append(
                 {
                    "id": c.id,
                    "user_id": c.user_id,
                    "content": c.content,
                    "created_at": c.created_at.isoformat() if getattr(c, "created_at", None) else None,
                    "user": {
                        "id": getattr(c_user, "id", None),
                        "username": getattr(c_user, "username", None),
                        "name": getattr(c_user, "name", None),
                        "avatar": getattr(c_user, "avatar", None),
                    } if c_user else None,
                }
            )

        likes = []
        for l in getattr(p, "likes", []) or []:
            l_user = getattr(l, "user", None)
            likes.append(
                {
                    "user_id": l.user_id,
                    "created_at": l.created_at.isoformat() if getattr(l, "created_at", None) else None,
                    "user": {
                        "id": getattr(l_user, "id", None),
                        "username": getattr(l_user, "username", None),
                        "name": getattr(l_user, "name", None),
                        "avatar": getattr(l_user, "avatar", None),
                    } if l_user else None,
                }
            )

        posts_data.append(
            {
                "id": p.id,
                "user_id": p.user_id,
                "caption": p.caption,
                "media_url": p.media_url,
                "media_type": p.media_type,
                "created_at": p.created_at.isoformat() if getattr(p, "created_at", None) else None,
                "user": post_user,
                "comments": comments,
                "likes": likes,
                "like_count": len(likes),
            }
        )

    return {"users": users_data, 
            "posts": posts_data}
