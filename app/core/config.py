# app/core/config.py (کد پیشنهادی و اصلاح شده)
from pydantic_settings import BaseSettings, SettingsConfigDict # این import کمی تغییر می‌کند
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Amirza Solver"
    APP_VERSION: str = "1.0.0"
    DEBUG_MODE: bool = False
    DATA_FILE_PATH: Path

    # این بخش جایگزین class Config شما می‌شود
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()