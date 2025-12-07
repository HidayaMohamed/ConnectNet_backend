# Import required SQLAlchemy tools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL (local file DB)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ConnectNet.db"

# Create database engine
# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory (used to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency used inside route functions to get a DB session
def get_db():
    db = SessionLocal()  # open connection
    try:
        yield db          # provide it to the route
    finally:
        db.close()        # close connection when done
