from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = os.getenv("APP_NAME", "Africa Sourcing Agent")
APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'africa_sourcing.db'}")
SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-before-deployment")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or None

if APP_ENV.lower() == "production" and SECRET_KEY == "development-only-change-before-deployment":
    raise RuntimeError("Set a strong SECRET_KEY in production before starting the application.")
