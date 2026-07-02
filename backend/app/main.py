from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.core.ml_client import load_recommender
from app.api import auth, movies, recommend

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Mandala API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(movies.router, tags=["Movies"])
app.include_router(recommend.router, tags=["Recommendations"])

@app.on_event("startup")
def startup_event():
    load_recommender()

@app.get("/")
def root():
    return {"message": "Welcome to Movie Mandala API"}