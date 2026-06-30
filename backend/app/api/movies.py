from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.movie import MovieResponse
from app.services.movie_service import get_all_movies, get_movie_by_id

router = APIRouter()


@router.get("/movies", response_model=List[MovieResponse])
def list_movies(search: Optional[str] = None, db: Session = Depends(get_db)):
    return get_all_movies(db, search)


@router.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = get_movie_by_id(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie