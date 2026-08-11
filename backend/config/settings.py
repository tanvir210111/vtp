"""
Pydantic BaseSettings management.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Video-to-Prompt API"
    API_V1_STR: str = "/api"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = ["*"]

    GEMINI_API_KEY: str = ""

    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STORAGE_DIR: str = os.path.abspath(os.path.join(BASE_DIR, "..", "storage"))
    OUTPUT_DIR: str = os.path.abspath(os.path.join(BASE_DIR, "..", "output"))

    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'sqlite.db')}"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()

# Make sure the runtime environment also sees the key for subprocesses and imported modules.
if settings.GEMINI_API_KEY:
    os.environ.setdefault("GEMINI_API_KEY", settings.GEMINI_API_KEY)
