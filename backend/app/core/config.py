import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database SQLite Path
SQLITE_DB_PATH = DATA_DIR / "pulse.db"
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH.as_posix()}"

PROJECT_NAME = "HFUT-PerceptPulse API"
API_V1_STR = "/api/v1"
