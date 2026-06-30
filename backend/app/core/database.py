from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# Connect to the database
engine = create_engine(DATABASE_URL)

# Used to create database sessions (talk to DB)
SessionLocal = sessionmaker(bind=engine)

# Used as the base class for all our table models
Base = declarative_base()

# This function gives a database session to each request, then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()