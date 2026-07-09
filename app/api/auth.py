from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import signup_user, login_user
from app.schemas.auth import ChangePassword
from app.core.security import get_current_user
from app.models.models import User
from app.services.auth_service import change_password
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

@router.put("/change-password")
def update_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = change_password(
        db,
        current_user,
        password_data.current_password,
        password_data.new_password,
        password_data.confirm_password
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )

    return result