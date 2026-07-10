# 🎬 Movie Mandala

Movie Mandala is a FastAPI-based movie recommendation web application that provides personalized movie recommendations using a **Content-Based Filtering** approach with **TF-IDF Vectorization** and **Cosine Similarity**.

The application features secure JWT authentication, a PostgreSQL (Supabase) database, an ML-powered recommendation engine, and a custom HTML/CSS/JavaScript frontend served directly by FastAPI.

---

# ✨ Features

- 🔐 JWT Authentication (Signup/Login)
- 🎥 Movie Search
- 🤖 Content-Based Movie Recommendation
- 🗄️ PostgreSQL Database (Supabase)
- ⚡ FastAPI REST API
- 🧠 TF-IDF + Cosine Similarity Recommendation Engine
- 🌐 Custom HTML, CSS & JavaScript Frontend
- 📦 Movie Catalog synchronized with ML artifacts
- 📄 Interactive Swagger Documentation (`/docs`)

---

# 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- JWT Authentication
- Python

### Machine Learning
- Pandas
- NumPy
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity

### Frontend
- HTML
- CSS
- JavaScript

---

# 📁 Project Structure

```
MovieMandala/
│
├── app/
│   ├── api/                 # FastAPI routes
│   ├── core/                # Config, database, security, ML loader
│   ├── data/                # Database seeding scripts
│   ├── domain/              # Domain models (ML)
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   │   └── ml/              # TF-IDF recommender & ML utilities
│   ├── static/              # CSS, JavaScript, images
│   ├── templates/           # HTML templates
│   └── main.py
│
├── artifacts/
│   ├── movie_catalog.parquet
│   ├── movie_index.joblib
│   ├── tfidf_matrix.joblib
│   └── tfidf_vectorizer.joblib
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── uv.lock
└── main.py
```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd MovieMandala
```

---

## 2. Install uv (recommended)

### Windows

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 3. Install dependencies

```bash
uv sync
```

---

## 4. Create environment file

Copy

```
.env.example
```

to

```
.env
```

and configure the following variables.

---

# ⚙️ Environment Variables

Required variables:

```
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TMDB_API_KEY=
```

### Notes

- `DATABASE_URL` → PostgreSQL/Supabase connection string
- `SECRET_KEY` → JWT signing key
- `TMDB_API_KEY` → Required only for the legacy TMDB seeding script

The application validates required environment variables during startup and provides clear error messages if any are missing.

---

# ▶️ Running the Application

```bash
uv run python main.py
```

or

```bash
uvicorn app.main:app --reload
```

Open:

Frontend

```
http://127.0.0.1:8000
```

Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

# 🗄️ Database Seeding

## Recommended Method

The application uses the same movie catalog as the trained recommendation model.

Import the complete movie catalog into PostgreSQL:

```bash
python -m app.data.seed_from_parquet
```

This imports approximately **5,992 movies** from

```
artifacts/movie_catalog.parquet
```

into the PostgreSQL (Supabase) database.

Because both the recommender and the database use the same TMDB IDs, every recommendation maps directly to a movie stored in the database.

---

## Legacy TMDB Seeding

A legacy seeding script is also included.

```bash
python -m app.data.seed_movies_tmdb
```

This imports a small sample of popular movies directly from the TMDB API.

It is intended for development/testing only.

---

# 🤖 Recommendation Workflow

1. User searches for a movie.
2. Movie details are retrieved from PostgreSQL.
3. The trained TF-IDF recommender loads the ML artifacts.
4. Cosine similarity identifies similar movies.
5. Recommended TMDB IDs are matched with database records.
6. Results are returned to the frontend.

---

# 🧠 Machine Learning Pipeline

The recommendation engine uses:

- TF-IDF Vectorization
- Cosine Similarity
- Pre-trained Scikit-learn artifacts
- Movie metadata including:
  - Overview
  - Genres
  - Keywords
  - Cast
  - Director

The trained model is stored inside the `artifacts/` folder and loaded automatically when the application starts.

---

# 🔐 Authentication

Movie Mandala uses JWT Bearer Authentication.

Supported endpoints:

- Signup
- Login
- Protected API endpoints

After login, the client receives a JWT access token which must be included in authenticated requests.

---

# 📡 API Endpoints

## Authentication

```
POST /signup
POST /login
```

## Movies

```
GET /movies
GET /movies/{movie_id}
```

## Recommendations

```
GET /recommend/{movie_id}
```

Interactive documentation:

```
/docs
```

---

# 📦 Artifacts

The `artifacts/` directory contains the trained recommendation model:

```
movie_catalog.parquet
movie_index.joblib
tfidf_matrix.joblib
tfidf_vectorizer.joblib
```

These files are required by the recommendation engine and should not be deleted.

---

# ✅ Improvements

Recent improvements include:

- Integrated backend, frontend, and ML into a single FastAPI application.
- Synchronized the PostgreSQL database with the same movie catalog used by the recommendation model.
- Added `seed_from_parquet.py` for importing the complete dataset (~5,992 movies).
- Improved configuration validation for missing environment variables.
- Fixed NumPy array handling in the recommender.
- Fixed authentication dependency issues.
- Pinned package versions for compatibility.
- Added Swagger documentation for API testing.
- Successfully tested authentication, movie search, and recommendation endpoints.

---

# 📌 Future Improvements

- Add user profile management.
- Support personalized recommendations based on user history.
- Expand the movie catalog with additional datasets.
- Improve search using fuzzy matching.
- Add movie trailers and reviews from TMDB.
- Deploy the application online.

---

# 👨‍💻 Developed By

Movie Mandala was developed as a **minor project** by a team of Computer Engineering students using FastAPI, Supabase, and Machine Learning.

---