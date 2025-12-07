from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Post, Comment, Like, User
from schemas import PostCreate
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    if not db.query(User).filter(User.id == post_data.user_id).first():
        raise HTTPException(status_code=404, detail="User not found")

    # Create the new Post object
    new_post = Post(
        user_id=post_data.user_id,
        caption=post_data.caption,
        media_url=post_data.media_url,
        media_type=post_data.media_type,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Return the created post
    return new_post
# Fetch all posts with user, comments, and likes
@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(
        joinedload(Post.user),     
        joinedload(Post.comments).joinedload(Comment.user),  
        joinedload(Post.likes).joinedload(Like.user)         
    ).all()

    
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "caption": post.caption,
            "media_url": post.media_url,
            "media_type": post.media_type,
            
            "created_at": post.created_at.isoformat() if post.created_at else None, 
            "user": {
                
            },
            "comments": [
                {
                    "id": comment.id,
                    "content": comment.content,
                    
                    "created_at": comment.created_at.isoformat() if comment.created_at else None, 
                    "user": {
                       
                    }
                } for comment in post.comments
            ],
            "likes": [
                {
                    "user": {
                       
                    }
                } for like in post.likes
            ]
        })
    print(f"Number of posts being returned: {len(result)}")
    return result
