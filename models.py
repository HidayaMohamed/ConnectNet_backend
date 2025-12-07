# SQLAlchemy imports
from sqlalchemy import Column, Text, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base

# User model (table = users)
class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Unique username & email
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Hashed password
    password = Column(String, nullable=False)

    # Optional profile fields
    name = Column(String)
    bio = Column(Text)
    avatar = Column(String)

    # Auto timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    followers = relationship("Follow", foreign_keys="[Follow.following_id]", back_populates="following")
    following = relationship("Follow", foreign_keys="[Follow.follower_id]", back_populates="follower")

# Post model
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    caption = Column(Text)
    media_url = Column(String)
    media_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Link to the user
    user = relationship("User", back_populates="posts")

    # Linked comments and likes
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

# Comment model
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")

# Like model
class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

# Follow model
class Follow(Base):
    __tablename__ = "follows"

    follower_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    following_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
