from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import auth
from app.models.models import User, Movie

# This creates your tables in Supabase if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Mandala API")

# Connect the auth routes we just made
app.include_router(auth.router, tags=["Authentication"])


@app.get("/")
def root():
    return {"message": "Welcome to Movie Mandala API"}