from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import auth, movies

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Mandala API")

# CORS setup — allow frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, etc.
    allow_headers=["*"],
)

# Connect routers
app.include_router(auth.router, tags=["Authentication"])
app.include_router(movies.router, tags=["Movies"])


@app.get("/")
def root():
    return {"message": "Welcome to Movie Mandala API"}