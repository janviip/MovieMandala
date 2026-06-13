from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas.user import UserCreate, LoginRequest

router = APIRouter()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
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


@router.post("/login")
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