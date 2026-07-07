# MovieMandala

Movie Mandala is a FastAPI-based movie recommender web app with:

- JWT (Bearer token) auth with signup/login
- PostgreSQL database (e.g. Supabase) via SQLAlchemy
- TMDB ingestion for the movie catalog
- TF-IDF vectorization + cosine similarity using scikit-learn
- Custom HTML, CSS, and JavaScript frontend, served directly by FastAPI

> This branch is the result of merging `backend-branch`, `frontend-branch`,
> and `ml-branch` into one runnable app. See "Known gaps" below for what's
> still left to do.

## Run locally

Install `uv` first.

```bash
# For macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# For Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then run the app:

```bash
cp .env.example .env   # fill in DATABASE_URL, SECRET_KEY, etc.
uv sync
uv run python main.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) — this serves the frontend
(redirects to `/result`). The interactive API docs are at
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Configuration

Required in `.env` (see `.env.example`):

- `DATABASE_URL` — Postgres/Supabase connection string
- `SECRET_KEY` — JWT signing secret
- `ALGORITHM` — e.g. `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — e.g. `30`
- `TMDB_API_KEY` — optional, only needed to run `app/data/seed_movies.py`

The app now fails fast with a clear error if any required variable is
missing, instead of crashing with an unhelpful `TypeError`.

## Seeding the database

`app/data/seed_movies.py` pulls ~100 popular movies from TMDB and inserts
them into the `movies` table (requires `TMDB_API_KEY`):

```bash
uv run python -m app.data.seed_movies
```

The `movie_id` used in the database is the TMDB id, which matches the
`tmdb_id` used by the trained recommender in `artifacts/`, so
`/recommend/{movie_id}` works directly against seeded movies.

## Architecture

- `app/core`: configuration, database, security, ML model loading
- `app/models`: SQLAlchemy entities (`User`, `Movie`)
- `app/schemas`: Pydantic request/response models
- `app/services`: auth, movie lookup, and the TF-IDF recommendation engine
- `app/services/ml`: TMDB ingestion, preprocessing, and the trained recommender class
- `app/api`: FastAPI routes (`/signup`, `/login`, `/movies`, `/recommend/{id}`)
- `app/static` and `app/templates`: frontend assets (CSS/JS and HTML pages)
- `artifacts/`: pre-trained TF-IDF model + catalog (built in `ml-branch`'s notebooks)

## Folder Structure

```text
movie-mandala/
├── app/
│   ├── api/              # FastAPI routes and request dependencies
│   ├── core/             # App configuration, database setup, security, ML loading
│   ├── data/             # TMDB seeding script
│   ├── domain/           # Domain models used by the recommender
│   ├── models/           # SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request and response schemas
│   ├── services/         # Auth, movie lookup, and recommendation logic
│   │   └── ml/           # TF-IDF recommender, TMDB client, preprocessing
│   ├── static/           # CSS and JavaScript assets
│   ├── templates/        # HTML pages (login, signup, result, about)
│   └── main.py           # FastAPI application factory and startup hooks
├── artifacts/             # Trained TF-IDF model, catalog, and lookup indexes
├── main.py                # Local entry point (runs uvicorn)
├── pyproject.toml         # Project metadata and Python dependencies
├── .env.example           # Example environment variables
└── README.md
```

## What changed in this merge

- Combined the backend API, the trained ML artifacts, and the static
  frontend into one app that FastAPI serves end-to-end.
- Fixed: empty `requirements.txt` — removed in favor of `pyproject.toml`
  as the single source of dependency truth (now includes `uvicorn`,
  `python-jose`, `passlib`, `email-validator`, `psycopg2-binary`, `requests`,
  which were missing).
- Fixed: `passlib`/`bcrypt` incompatibility that made **every signup crash**
  with a 500 error (bcrypt ≥4.1 removed an attribute passlib's version
  detection relies on) — pinned `bcrypt==4.0.1`.
- Fixed: a numpy-array truthiness crash in the recommender
  (`app/services/ml/tfidf_recommender.py`) that made **every recommendation
  request return "No recommendations found"** — `genres` is stored as a
  numpy array per row, and `array or ()` raises
  `ValueError: truth value of an array... is ambiguous`. Rewrote the
  null-handling for `genres`, `vote_average`, and `popularity`.
- Removed two empty, unused files: `app/data/sample_movies.json` and
  `app/services/recommendation_service.py`.
- Added validation in `app/core/config.py` so a missing `.env` variable
  fails immediately with a clear message instead of crashing deep inside
  `int(None)`.
- Pinned `scikit-learn==1.9.0` to match the version the bundled artifacts
  were trained with (avoids an `InconsistentVersionWarning`/potential
  scoring drift on a mismatched install).
- All four endpoints (`/signup`, `/login`, `/movies`, `/recommend/{id}`)
  were manually tested end-to-end against a live server, including auth
  failure cases (wrong password, missing token, duplicate email).

## Known gaps (next steps)

- **Frontend is still static.** `app/static/js/app.js` is empty — the
  login/signup pages don't call the API yet, and `result.html` renders a
  hardcoded fake movie list instead of calling `/movies` and
  `/recommend/{id}`. This is the next piece of work.
- **Auth storage strategy isn't decided.** The backend issues a Bearer
  token (`Authorization: Bearer <token>`) rather than a cookie; the
  frontend will need to store this (e.g. `localStorage`) and attach it to
  requests once wired up.
- The bundled catalog is only 200 movies (from the `ml-branch` notebooks).
  Re-run the ingestion notebook with more TMDB pages for broader coverage.
