from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from app.core.database import Base, engine
from app.core.ml_client import load_recommender
from app.api import auth, movies, recommend

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Mandala API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routers (all prefixed implicitly by their own paths, e.g. /signup, /login, /movies, /recommend/{id})
app.include_router(auth.router, tags=["Authentication"])
app.include_router(movies.router, tags=["Movies"])
app.include_router(recommend.router, tags=["Recommendations"])

# Static assets: CSS, JS, images -> served at /static/...
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def startup_event():
    load_recommender()


# ---- Frontend page routes (serve the plain HTML pages from app/templates) ----

@app.get("/")
def root():
    return RedirectResponse(url="/result")


@app.get("/result")
def result_page():
    return FileResponse(TEMPLATES_DIR / "result.html")


@app.get("/login")
def login_page():
    return FileResponse(TEMPLATES_DIR / "login.html")


@app.get("/signup")
def signup_page():
    return FileResponse(TEMPLATES_DIR / "signup.html")


@app.get("/about")
def about_page():
    return FileResponse(TEMPLATES_DIR / "about.html")


# ---- API status endpoint (moved off "/" since that now serves the frontend) ----

@app.get("/api/status")
def api_status():
    return {"message": "Welcome to Movie Mandala API"}
