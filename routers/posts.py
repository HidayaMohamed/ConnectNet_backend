from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Post, Comment, Like, User
from schemas import PostCreate

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == post_data.user_id).first()
    if not user:
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
        "created_at": new_post.created_at.isoformat() if new_post.created_at else None,
    }

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(
        joinedload(Post.user),
        joinedload(Post.comments).joinedload(Comment.user),
        joinedload(Post.likes).joinedload(Like.user),
    ).all()

    result = []
    for post in posts:
        user_data = {
            "id": post.user.id,
            "username": post.user.username,
            "name": post.user.name,
            "avatar": post.user.avatar,
        } if post.user else None

        comments = [
            {
                "id": c.id,
                "content": c.content,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "user": {
                    "id": c.user.id,
                    "username": c.user.username,
                    "name": c.user.name,
                    "avatar": c.user.avatar,
                } if c.user else None,
            }
            for c in post.comments
        ]

        likes = [
            {
                
                "user": {
                    "id": l.user.id,
                    "username": l.user.username,
                    "name": l.user.name,
                    "avatar": l.user.avatar,
                } if l.user else None,
            }
            for l in post.likes
        ]

        result.append({
            "id": post.id,
            "caption": post.caption,
            "media_url": post.media_url,
            "media_type": post.media_type,
            "created_at": post.created_at.isoformat() if post.created_at else None,
            "user": user_data,
            "comments": comments,
            "likes": likes,
            "like_count": len(likes),
        })

    return result
