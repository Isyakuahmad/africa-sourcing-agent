from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'africa_sourcing.db'}")
APP_NAME = os.getenv("APP_NAME", "Africa Sourcing Agent")
SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
