from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.core.ml_client import get_recommendations
from app.models.models import User

router = APIRouter()

@router.get("/recommend/{movie_id}")
def recommend(
    movie_id: int,
    current_user: User = Depends(get_current_user)
):
    results = get_recommendations(movie_id, k=10)
    if not results:
        raise HTTPException(
            status_code=404,
            detail="No recommendations found. ML model may not be trained yet."
        )
    return results