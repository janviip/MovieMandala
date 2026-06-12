from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User

app = FastAPI(title="Movie Mandala")

# Create DB tables
Base.metadata.create_all(bind=engine)

# -----------------------------
# Database Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Request Schemas
# -----------------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def home():
    return {"message": "Movie Mandala running"}

@app.get("/test")
def test():
    return {"status": "API working"}

# -----------------------------
# SIGNUP API
# -----------------------------
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
        "message": "User created successfully",
        "user_id": new_user.id
    }

# -----------------------------
# LOGIN API
# -----------------------------
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