from pydantic import BaseModel
from typing import Optional

class MovieResponse(BaseModel):
    movie_id: int
    title: str
    overview: Optional[str] = None
    genres: Optional[str] = None
    cast: Optional[str] = None
    director: Optional[str] = None
    poster_url: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None

    class Config:
        from_attributes = True