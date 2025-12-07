from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Post, Comment, Like, User

router = APIRouter(prefix="/posts", tags=["Posts"])

# Fetch all posts with user, comments, and likes
@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(
        joinedload(Post.user),       # load user who created post
        joinedload(Post.comments).joinedload(Comment.user),  # load comment user
        joinedload(Post.likes).joinedload(Like.user)         # load like user
    ).all()

    # Convert to JSON-friendly format
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "caption": post.caption,
            "media_url": post.media_url,
            "media_type": post.media_type,
            "created_at": post.created_at,
            "user": {
                "id": post.user.id,
                "username": post.user.username,
                "avatar": post.user.avatar
            },
            "comments": [
                {
                    "id": comment.id,
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "user": {
                        "id": comment.user.id,
                        "username": comment.user.username,
                        "avatar": comment.user.avatar
                    }
                } for comment in post.comments
            ],
            "likes": [
                {
                    "user": {
                        "id": like.user.id,
                        "username": like.user.username,
                        "avatar": like.user.avatar
                    }
                } for like in post.likes
            ]
        })
    return result
