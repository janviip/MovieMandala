from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.ml_client import get_recommendations

from app.models.models import User, Movie

router = APIRouter()


@router.get("/recommend/{movie_id}")
def recommend(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    results = get_recommendations(movie.title, k=10)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found."
        )

    return results