from __future__ import annotations

import pandas as pd


def load_demo_catalog() -> pd.DataFrame:
    """
    Tiny fallback catalog for local testing without TMDB credentials.

    Replace this with your existing bundled demo catalog if you already have one.
    """
    rows = [
        {
            "tmdb_id": 603,
            "title": "The Matrix",
            "overview": "A hacker discovers reality is a simulated world controlled by machines.",
            "release_date": "1999-03-31",
            "popularity": 100.0,
            "vote_average": 8.2,
            "vote_count": 25000,
            "genres": ("Action", "Science Fiction"),
            "keywords": ("simulation", "artificial intelligence", "cyberpunk"),
            "cast": ("Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"),
            "directors": ("Lana Wachowski", "Lilly Wachowski"),
            "poster_path": None,
        },
        {
            "tmdb_id": 27205,
            "title": "Inception",
            "overview": "A thief enters dreams to steal secrets and is given a chance to erase his past.",
            "release_date": "2010-07-16",
            "popularity": 120.0,
            "vote_average": 8.4,
            "vote_count": 36000,
            "genres": ("Action", "Science Fiction", "Thriller"),
            "keywords": ("dream", "subconscious", "heist"),
            "cast": ("Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"),
            "directors": ("Christopher Nolan",),
            "poster_path": None,
        },
        {
            "tmdb_id": 157336,
            "title": "Interstellar",
            "overview": "Explorers travel through a wormhole in space to save humanity.",
            "release_date": "2014-11-07",
            "popularity": 115.0,
            "vote_average": 8.4,
            "vote_count": 35000,
            "genres": ("Adventure", "Drama", "Science Fiction"),
            "keywords": ("space travel", "wormhole", "future"),
            "cast": ("Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"),
            "directors": ("Christopher Nolan",),
            "poster_path": None,
        },
        {
            "tmdb_id": 550,
            "title": "Fight Club",
            "overview": "An office worker forms an underground fight club with a charismatic stranger.",
            "release_date": "1999-10-15",
            "popularity": 95.0,
            "vote_average": 8.4,
            "vote_count": 29000,
            "genres": ("Drama", "Thriller"),
            "keywords": ("identity", "insomnia", "underground"),
            "cast": ("Brad Pitt", "Edward Norton", "Helena Bonham Carter"),
            "directors": ("David Fincher",),
            "poster_path": None,
        },
    ]
    return pd.DataFrame(rows)
