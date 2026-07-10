from pydantic import BaseModel, EmailStr

# What the user SENDS when signing up
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# What the user SENDS when logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# What we SEND BACK after successful login (a token)
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str