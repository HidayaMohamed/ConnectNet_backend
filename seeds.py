from database import SessionLocal, engine, Base
from models import User, Post, Comment, Like, Follow
from passlib.context import CryptContext
from sqlalchemy import or_

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        users_data = [
            {"username": "alice", "email": "alice@example.com", "password": "password123", "name": "Alice"},
            {"username": "bob", "email": "bob@example.com", "password": "password123", "name": "Bob"},
            {"username": "charlie", "email": "charlie@example.com", "password": "password123", "name": "Charlie"},
        ]

        created_users = {}
        for u in users_data:
            existing = db.query(User).filter(or_(User.username == u["username"], User.email == u["email"])).first()
            if existing:
                created_users[u["username"]] = existing
                continue
            hashed = pwd_context.hash(u["password"])
            new_user = User(username=u["username"], email=u["email"], password=hashed, name=u["name"])
            db.add(new_user)
            db.flush()
            created_users[u["username"]] = new_user
            db.commit()

        posts_data = [
            {"user": "alice", "caption": "Hello, world!", "media_url": None, "media_type": None},
            {"user": "bob", "caption": "This is my first post!", "media_url": "https://example.com/photo.jpg", "media_type": "image"},
        ]

        created_posts = {}
        for p in posts_data:
            user_obj = created_users.get(p["user"]) or db.query(User).filter(User.username == p["user"]).first()
            if not user_obj:
                continue
            existing_post = db.query(Post).filter(Post.user_id == user_obj.id, Post.caption == p["caption"]).first()
            if existing_post:
                created_posts[p["caption"]] = existing_post
                continue
            post = Post(user_id=user_obj.id, caption=p["caption"], media_url=p["media_url"], media_type=p["media_type"])
            db.add(post)
            db.flush()
            created_posts[p["caption"]] = post
        db.commit()

        comment_items = [
            {"user": "bob", "post_caption": "Hello, world!", "content": "Nice post!"},
            {"user": "charlie", "post_caption": "Hello, world!", "content": "Welcome!"},
        ]
        for c in comment_items:
            user_obj = db.query(User).filter(User.username == c["user"]).first()
            post_obj = db.query(Post).filter(Post.caption == c["post_caption"]).first()
            if not user_obj or not post_obj:
                continue
            exists = db.query(Comment).filter(Comment.user_id == user_obj.id, Comment.post_id == post_obj.id, Comment.content == c["content"]).first()
            if exists:
                continue
            comment = Comment(user_id=user_obj.id, post_id=post_obj.id, content=c["content"])
            db.add(comment)
        db.commit()

        likes = [
            {"user": "bob", "post_caption": "Hello, world!"},
            {"user": "alice", "post_caption": "This is my first post!"},
        ]
        for l in likes:
            user_obj = db.query(User).filter(User.username == l["user"]).first()
            post_obj = db.query(Post).filter(Post.caption == l["post_caption"]).first()
            if not user_obj or not post_obj:
                continue
            exists = db.query(Like).filter(Like.user_id == user_obj.id, Like.post_id == post_obj.id).first()
            if exists:
                continue
            like = Like(user_id=user_obj.id, post_id=post_obj.id)
            db.add(like)
        db.commit()

        print("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print("Error seeding data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

    