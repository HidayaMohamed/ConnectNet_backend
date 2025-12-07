from pydantic import BaseModel

# Schema used when creating a post
class PostCreate(BaseModel):
    user_id: int # ID of the user creating the post (you might get this from auth later)
    caption: str
    media_url: str = None
    media_type: str = None