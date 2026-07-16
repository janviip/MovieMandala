from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.models import Movie
from app.services.ml.tmdb_client import TMDBClient



def get_all_movies(
    db: Session,
    search: str = None
):

    # First check local database

    query = db.query(Movie)


    if search:

        query = query.filter(
            or_(
            Movie.title.ilike(f"%{search}%"),
            Movie.overview.ilike(f"%{search}%"),
            Movie.genres.ilike(f"%{search}%"),
            Movie.keywords.ilike(f"%{search}%"),
            Movie.cast.ilike(f"%{search}%"),
            Movie.director.ilike(f"%{search}%")
        )
        )


    movies = query.all()


    if movies:
        return movies



    # If not found, search TMDB

    if search:

        client = TMDBClient()


        response = client.search_movies(search)


        tmdb_movies = []


        for movie in response.get("results", []):


            tmdb_movies.append({

                "movie_id":
                    movie.get("id"),


                "title":
                    movie.get("title"),


                "overview":
                    movie.get("overview"),


                "genres":
                    None,


                "poster_url":

                    (
                        "https://image.tmdb.org/t/p/w500"
                        + movie["poster_path"]

                        if movie.get("poster_path")

                        else None
                    ),


                "release_date":
                    movie.get("release_date"),


                "vote_average":
                    movie.get("vote_average")

            })


        return tmdb_movies



    return []





def get_movie_by_id(
    db: Session,
    movie_id: int
):

    return db.query(Movie).filter(
        Movie.movie_id == movie_id
    ).first()

def get_movie_suggestions(
    db: Session,
    search: str
):
    if not search or len(search.strip()) < 2:
        return []

    search = search.strip()

    movies = (
        db.query(Movie)
        .filter(Movie.title.ilike(f"%{search}%"))
        .order_by(Movie.vote_average.desc())
        .limit(8)
        .all()
    )

    return [
        {
            "movie_id": movie.movie_id,
            "title": movie.title,
            "poster_url": movie.poster_url,
            "release_date": movie.release_date,
        }
        for movie in movies
    ]