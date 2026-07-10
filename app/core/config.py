import os
from dotenv import load_dotenv

load_dotenv()  # reads the .env file

REQUIRED_VARS = ["DATABASE_URL", "SECRET_KEY", "ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES"]
missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    raise RuntimeError(
        f"Missing required environment variable(s): {', '.join(missing)}. "
        "Copy .env.example to .env and fill in the values."
    )

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
except ValueError:
    raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer.")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
