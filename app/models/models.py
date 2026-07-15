from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    watchlist = relationship("Watchlist", back_populates="user")


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

    watchlist = relationship("Watchlist", back_populates="movie")

class Watchlist(Base):
    __tablename__ = "watchlist"

    watchlist_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    movie_id = Column(
        Integer,
        ForeignKey("movies.movie_id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship("User", back_populates="watchlist")
    movie = relationship("Movie", back_populates="watchlist")