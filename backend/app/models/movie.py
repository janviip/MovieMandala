from sqlalchemy import Column, Integer, String
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    genre = Column(String(100))
    description = Column(String(1000))