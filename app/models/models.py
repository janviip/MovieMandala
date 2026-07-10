from sqlalchemy import Column, Integer, String, Float, Text
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    overview = Column(Text)
    genres = Column(String)
    keywords = Column(String)
    cast = Column(String)
    director = Column(String)
    poster_url = Column(String)
    release_date = Column(String)
    vote_average = Column(Float)