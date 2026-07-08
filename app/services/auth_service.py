from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.auth import UserCreate, UserLogin
from app.core.security import hash_password, verify_password, create_access_token


def signup_user(db: Session, user_data: UserCreate):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None  # we'll handle the error message in the route

    # Create new user with hashed password
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, login_data: UserLogin):
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        return None

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        return None

    # Create JWT token
    token = create_access_token(
        {
            "user_id": user.user_id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username
    }