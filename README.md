# MovieMandala

Movie Mandala is a FastAPI-based movie recommender web app with:

- JWT cookie auth with signup/login
- SQLite persistence for users, cached movies, and recommendation history
- TMDB ingestion for the movie catalog
- TF-IDF vectorization + cosine similarity using scikit-learn
- Custom HTML, CSS, and vanilla JavaScript frontend

## Run locally

Install `uv` first.

```bash
# For macOS/ Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then run the app:

```bash
cp .env.example .env
uv sync
uv run python main.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Configuration

Set either `TMDB_API_KEY` or `TMDB_API_READ_TOKEN` in `.env`.

If TMDB credentials are not set, the app falls back to a bundled demo catalog so the UI and recommender still work.

## Architecture

The project is split into:

- `app/core`: configuration, database, security
- `app/models`: SQLAlchemy entities
- `app/repositories`: persistence interfaces and implementations
- `app/services`: auth, TMDB sync, and recommendation logic
- `app/api`: FastAPI routes and dependencies
- `app/templates` and `app/static`: frontend assets

## Folder Structure

```text
movie-mandala/
├── app/
│   ├── api/              # FastAPI routes and request dependencies
│   ├── core/             # App configuration, database setup, and security
│   ├── data/             # Bundled demo movie catalog
│   ├── domain/           # Domain models used by the recommender
│   ├── models/           # SQLAlchemy ORM models
│   ├── repositories/     # Persistence interfaces and SQLAlchemy implementations
│   ├── schemas/          # Pydantic request and response schemas
│   ├── services/         # Auth, movie ingestion, and recommendation logic
│   ├── static/           # CSS and JavaScript assets
│   ├── templates/        # HTML templates
│   └── main.py           # FastAPI application factory and startup hooks
├── main.py               # Local entry point
├── pyproject.toml        # Project metadata and Python dependencies
├── uv.lock               # Locked dependency versions
├── .env.example          # Example environment variables
└── README.md
```
