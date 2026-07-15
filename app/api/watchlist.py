from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Movie, Watchlist

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.get("/check/{movie_id}")
def check_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == current_user.user_id,
            Watchlist.movie_id == movie_id
        )
        .first()
    )

    return {
        "in_watchlist": item is not None
    }
@router.post("/{movie_id}")
def add_to_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check movie exists
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Check duplicate
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.movie_id == movie_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Movie already in watchlist")

    watchlist = Watchlist(
        user_id=current_user.user_id,
        movie_id=movie_id
    )

    db.add(watchlist)
    db.commit()

    return {"message": "Movie added to watchlist"}

@router.get("/")
def get_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    watchlist = (
        db.query(Watchlist)
        .filter(Watchlist.user_id == current_user.user_id)
        .all()
    )

    movies = []

    for item in watchlist:
        movie = db.query(Movie).filter(Movie.movie_id == item.movie_id).first()

        if movie:
            movies.append({
                "movie_id": movie.movie_id,
                "title": movie.title,
                "poster_url": movie.poster_url,
                "vote_average": movie.vote_average,
                "release_date": movie.release_date
            })

    return movies

@router.delete("/{movie_id}")
def remove_from_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = (
        db.query(Watchlist)
        .filter(
            Watchlist.user_id == current_user.user_id,
            Watchlist.movie_id == movie_id
        )
        .first()
    )

    if not item:
        raise HTTPException(status_code=404, detail="Movie not found in watchlist")

    db.delete(item)
    db.commit()

    return {"message": "Movie removed from watchlist"}