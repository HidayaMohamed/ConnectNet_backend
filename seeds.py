# seeds.py
from database import SessionLocal, engine, Base
from models import User, Post, Comment, Like, Follow
from passlib.context import CryptContext

# Match the algorithm used in auth.py and users.py
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    try:
        # --- Create Users ---
        # **CRITICAL: HASH THE PASSWORDS HERE**
        hashed_password_1 = pwd_context.hash("password123")
        hashed_password_2 = pwd_context.hash("password123")
        hashed_password_3 = pwd_context.hash("password123")

        user1 = User(username="alice", email="alice@example.com", password=hashed_password_1, name="Alice")
        user2 = User(username="bob", email="bob@example.com", password=hashed_password_2, name="Bob")
        user3 = User(username="charlie", email="charlie@example.com", password=hashed_password_3, name="Charlie")

        db.add_all([user1, user2, user3])
        db.commit()

        # Get IDs for relationships
        alice_id = user1.id
        bob_id = user2.id
        charlie_id = user3.id

        # --- Create Posts ---
        post1 = Post(user_id=alice_id, caption="Hello, world!", media_url=None, media_type=None)
        post2 = Post(user_id=bob_id, caption="This is my first post!", media_url="https://example.com/photo.jpg", media_type="image")
        
        db.add_all([post1, post2])
        db.commit()
        
        post1_id = post1.id
        post2_id = post2.id

        # --- Create Comments ---
        comment1 = Comment(user_id=bob_id, post_id=post1_id, content="Nice post!")
        comment2 = Comment(user_id=charlie_id, post_id=post1_id, content="Welcome!")

        db.add_all([comment1, comment2])
        db.commit()

        # --- Create Likes ---
        like1 = Like(user_id=bob_id, post_id=post1_id)
        like2 = Like(user_id=alice_id, post_id=post2_id)
        
        db.add_all([like1, like2])
        db.commit()

        print("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print("Error seeding data:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()