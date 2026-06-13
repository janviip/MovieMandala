from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app.models import User, Movie

from pydantic import BaseModel

app = FastAPI(title="Movie Mandala")

# IMPORTANT: create tables ONCE
Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class MovieCreate(BaseModel):
    title: str
    genre: str
    description: str

# ---------------- HOME ----------------
@app.get("/")
def home():
    return {"message": "Movie Mandala running"}


# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "id": new_user.id
    }

# ---------------- LOGIN ----------------
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == data.email,
        User.password == data.password
    ).first()

    if not user:
        return {"message": "Invalid credentials"}

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }
#---------------- ADD MOVIE ----------------
@app.post("/movies")
def add_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    new_movie = Movie(
        title=movie.title,
        genre=movie.genre,
        description=movie.description
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return {
        "message": "Movie added",
        "movie_id": new_movie.id
    }
#---------------- GET MOVIES ----------------
@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):

    movies = db.query(Movie).all()

    return movies

#---------------- GET single MOVIE ----------------
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        return {"message": "Movie not found"}

    return movie