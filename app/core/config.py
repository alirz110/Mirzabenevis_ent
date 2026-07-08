
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Amirza Solver"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    DATA_FILE_PATH: Path

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
