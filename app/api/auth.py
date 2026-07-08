from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import signup_user, login_user

router = APIRouter()


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = signup_user(db, user_data)
    if new_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully", "user_id": new_user.user_id}


@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    result = login_user(db, login_data)

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return result