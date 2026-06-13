from fastapi import FastAPI

from app.database import Base, engine
from app.models import User, Movie
from app.routers import auth

app = FastAPI(title="Movie Mandala")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "Movie Mandala running"}