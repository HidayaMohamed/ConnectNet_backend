from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Post, Comment, Like, User
from schemas import PostCreate

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    if not db.query(User).filter(User.id == post_data.user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_post = Post(
        user_id=post_data.user_id,
        caption=post_data.caption,
        media_url=post_data.media_url,
        media_type=post_data.media_type,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "id": new_post.id,
        "user_id": new_post.user_id,
        "caption": new_post.caption,
        "media_url": new_post.media_url,
        "media_type": new_post.media_type,
        "created_at": new_post.created_at.isoformat() if getattr(new_post, "created_at", None) else None,
    }

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(
        joinedload(Post.user),
        joinedload(Post.comments).joinedload(Comment.user),
        joinedload(Post.likes).joinedload(Like.user)
    ).all()

    result = []
    for post in posts:
        user = getattr(post, "user", None)
        user_data = {
            "id": getattr(user, "id", None),
            "username": getattr(user, "username", None),
            "name": getattr(user, "name", None),
            "avatar": getattr(user, "avatar", None),
        } if user else None

        comments = []
        for comment in getattr(post, "comments", []) or []:
            cuser = getattr(comment, "user", None)
            comments.append({
                "id": comment.id,
                "content": comment.content,
                "created_at": comment.created_at.isoformat() if getattr(comment, "created_at", None) else None,
                "user": {
                    "id": getattr(cuser, "id", None),
                    "username": getattr(cuser, "username", None),
                    "name": getattr(cuser, "name", None),
                    "avatar": getattr(cuser, "avatar", None),
                } if cuser else None
            })

        likes = []
        for like in getattr(post, "likes", []) or []:
            luser = getattr(like, "user", None)
            likes.append({
                "id": like.id,
                "user": {
                    "id": getattr(luser, "id", None),
                    "username": getattr(luser, "username", None),
                    "name": getattr(luser, "name", None),
                    "avatar": getattr(luser, "avatar", None),
                } if luser else None
            })

        result.append({
            "id": post.id,
            "caption": post.caption,
            "media_url": post.media_url,
            "media_type": post.media_type,
            "created_at": post.created_at.isoformat() if getattr(post, "created_at", None) else None,
            "user": user_data,
            "comments": comments,
            "likes": likes,
            "like_count": len(likes),
        })

    return result