from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    genre: str
    description: str