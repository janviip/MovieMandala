import requests
from app.core.config import TMDB_API_KEY
from app.core.database import SessionLocal
from app.models.models import Movie

BASE_URL = "https://api.themoviedb.org/3"

def fetch_popular_movies(pages=300):
    all_movies = []
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/movie/popular"
        params = {"api_key": TMDB_API_KEY, "page": page}
        response = requests.get(url, params=params)
        data = response.json()
        all_movies.extend(data["results"])
    return all_movies


def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY, "append_to_response": "credits,keywords"}
    response = requests.get(url, params=params)
    return response.json()


def seed_database():
    db = SessionLocal()
    movies = fetch_popular_movies(pages=300)  # 300 pages = ~6000 movies

    for m in movies:
        details = get_movie_details(m["id"])

        genres = ", ".join([g["name"] for g in details.get("genres", [])])
        keywords = ", ".join([k["name"] for k in details.get("keywords", {}).get("keywords", [])])
        cast = ", ".join([c["name"] for c in details.get("credits", {}).get("cast", [])[:5]])
        director = next(
            (c["name"] for c in details.get("credits", {}).get("crew", []) if c["job"] == "Director"),
            ""
        )

        movie = Movie(
            movie_id=m["id"],
            title=m["title"],
            overview=m.get("overview", ""),
            genres=genres,
            keywords=keywords,
            cast=cast,
            director=director,
            poster_url=f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None,
            release_date=m.get("release_date", ""),
            vote_average=m.get("vote_average", 0.0)
        )

        existing = db.query(Movie).filter(Movie.movie_id == m["id"]).first()
        if not existing:
            db.add(movie)

    db.commit()
    db.close()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()