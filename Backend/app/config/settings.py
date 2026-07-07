from functools import lru_cache
from pathlib import Path
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = os.getenv(
    "APP_ENV_FILE",
    BASE_DIR / ".env"
)


class Settings(BaseSettings):

    # =====================================================
    # APPLICATION
    # =====================================================

    APP_NAME: str
    APP_VERSION: str
    ENV: str
    DEBUG: bool

    # =====================================================
    # SERVER
    # =====================================================

    HOST: str
    BACKEND_PORT: int

    FRONTEND_URL: str

    # =====================================================
    # DATABASE
    # =====================================================

    DATABASE_URL: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # =====================================================
    # JWT
    # =====================================================

    JWT_SECRET: str
    JWT_ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    # =====================================================
    # OLLAMA
    # =====================================================

    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str
    OLLAMA_EMBED_MODEL: str

    # =====================================================
    # WEAVIATE
    # =====================================================

    WEAVIATE_URL: str
    WEAVIATE_CLASS: str

    # =====================================================
    # FILE UPLOAD
    # =====================================================

    UPLOAD_DIR: str
    MAX_UPLOAD_SIZE: int

    # =====================================================
    # RAG
    # =====================================================

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    TOP_K: int

    # =====================================================
    # LOGGING
    # =====================================================

    LOG_LEVEL: str
    LOG_DIR: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings() # pyright: ignore


settings = get_settings()