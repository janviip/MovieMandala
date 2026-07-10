import pandas as pd

from app.core.database import SessionLocal
from app.models.models import Movie

def clean_value(value):
    """Convert lists/arrays to comma-separated strings and handle nulls."""
    if value is None:
        return ""

    if isinstance(value, float) and pd.isna(value):
        return ""

    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)

    # Handle NumPy arrays
    if hasattr(value, "tolist"):
        value = value.tolist()
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)

    return str(value)
# Read parquet
df = pd.read_parquet("artifacts/movie_catalog.parquet")

print(f"Found {len(df)} movies in parquet.")

db = SessionLocal()

inserted = 0
skipped = 0

for index, row in df.iterrows():

    movie_id = int(row["tmdb_id"])

    existing = (
        db.query(Movie)
        .filter(Movie.movie_id == movie_id)
        .first()
    )

    if existing:
        skipped += 1
        continue

    movie = Movie(
    movie_id=movie_id,
    title=clean_value(row["title"]),
    overview=clean_value(row["overview"]),
    genres=clean_value(row["genres"]),
    keywords=clean_value(row["keywords"]),
    cast=clean_value(row["cast"]),
    director=clean_value(row["directors"]),
    poster_url=(
        f"https://image.tmdb.org/t/p/w500{row['poster_path']}"
        if clean_value(row["poster_path"]) != ""
        else None
    ),
    release_date=clean_value(row["release_date"]),
    vote_average=float(row["vote_average"]) if pd.notna(row["vote_average"]) else 0.0,
)
    db.add(movie)
    inserted += 1

    # Commit every 100 movies
    if inserted % 100 == 0:
        db.commit()
        print(f"Inserted {inserted} new movies...")

# Final commit
db.commit()
db.close()

print("===================================")
print(f"Inserted : {inserted}")
print(f"Skipped  : {skipped}")
print("Done!")