
from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from .. import models, database 
from pydantic import BaseModel
 

router = APIRouter()

class LikeCreate(BaseModel):
    user_id: int 
    post_id: int 

def get_db():
    db = database.SessionLocal() 
    try: 
        yield db
    finally:  
        db.close() 

@router.post("/") 
def like_post(like: LikeCreate, db: Session = Depends(get_db)):
    # check if like already exists
    existing_like = db.query(models.Like).filter(
        models.Like.user_id == like.user_id,
        models.Like.post_id == like.post_id
    ).first()  
    if existing_like: 
        raise HTTPException(status_code=400, detail="Already liked")
     
    new_like = models.Like(
        user_id=like.user_id,
        post_id=like.post_id 
    ) 
    db.add(new_like)
    db.commit() 
    return {"user_id": like.user_id, "post_id": like.post_id, "status": "liked"}
 
@router.delete("/")
def unlike_post(like: LikeCreate, db: Session = Depends(get_db)):
    existing_like = db.query(models.Like).filter(
        models.Like.user_id == like.user_id,
        models.Like.post_id == like.post_id
    ).first() 
    if not existing_like:
        raise HTTPException(status_code=404, detail="Like not found")
     
    db.delete(existing_like)
    db.commit() 
    return {"status": "unliked"} 
 