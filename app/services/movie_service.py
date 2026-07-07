from sqlalchemy.orm import Session
from app.models.models import Movie


def get_all_movies(db: Session, search: str = None):
    query = db.query(Movie)
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    return query.all()


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.movie_id == movie_id).first()