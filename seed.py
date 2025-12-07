from database import SessionLocal, engine, Base
from models import User, Post, Comment, Like, Follow

# Create all tables (if not already created via Alembic)
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()

    try:
        # --- Create Users ---
        user1 = User(username="alice", email="alice@example.com", password="password1", name="Alice")
        user2 = User(username="bob", email="bob@example.com", password="password2", name="Bob")
        user3 = User(username="charlie", email="charlie@example.com", password="password3", name="Charlie")

        db.add_all([user1, user2, user3])
        db.commit()

        # --- Create Posts ---
        post1 = Post(user_id=user1.id, caption="Hello, world!", media_url=None, media_type=None)
        post2 = Post(user_id=user2.id, caption="This is my first post!", media_url="https://example.com/photo.jpg", media_type="image")
        post3 = Post(user_id=user3.id, caption="Enjoying the sunny weather", media_url=None, media_type=None)

        db.add_all([post1, post2, post3])
        db.commit()

        # --- Create Comments ---
        comment1 = Comment(user_id=user2.id, post_id=post1.id, content="Nice post!")
        comment2 = Comment(user_id=user3.id, post_id=post1.id, content="Welcome!")
        comment3 = Comment(user_id=user1.id, post_id=post2.id, content="Great photo!")

        db.add_all([comment1, comment2, comment3])
        db.commit()

        # --- Create Likes ---
        like1 = Like(user_id=user2.id, post_id=post1.id)
        like2 = Like(user_id=user3.id, post_id=post1.id)
        like3 = Like(user_id=user1.id, post_id=post2.id)

        db.add_all([like1, like2, like3])
        db.commit()

        # --- Create Follows ---
        follow1 = Follow(follower_id=user2.id, following_id=user1.id)
        follow2 = Follow(follower_id=user3.id, following_id=user1.id)
        follow3 = Follow(follower_id=user1.id, following_id=user2.id)

        db.add_all([follow1, follow2, follow3])
        db.commit()

        print("Seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print("Error seeding data:", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
