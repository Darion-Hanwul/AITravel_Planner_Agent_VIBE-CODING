from functools import lru_cache
from pathlib import Path
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# Mendapatkan direktori dasar 'Backend/' dari letak file ini
BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = os.getenv(
    "APP_ENV_FILE",
    BASE_DIR / ".env"
)


class Settings(BaseSettings):
    """
    Settings mengelola seluruh konfigurasi lingkungan aplikasi secara global.

    Responsibility
    --------------
    - Memuat variabel dari berkas Backend/.env secara strongly-typed.
    - Menyediakan konfigurasi untuk server, database, model AI (Ollama), dan VDB (Weaviate).
    - Menyediakan ambang batas (threshold) untuk guardrails keamanan input LLM.
    """

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
    WEAVIATE_GRPC_PORT: int = 50051
    WEAVIATE_PORT: int = 8080

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

    # =====================================================
    # WEATHER
    # =====================================================
    WEATHER_CACHE_EXPIRE_MINUTES: int = 15
    OPENWEATHER_API_KEY: str = ""
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    # =====================================================
    # CURRENCY
    # =====================================================
    EXCHANGERATE_API_KEY: str = ""
    EXCHANGERATE_BASE_URL: str = "https://v6.exchangerate-api.com/v6"
    CURRENCY_CACHE_EXPIRE_MINUTES: int = 15

    # =====================================================
    # PLACE SEARCH
    # =====================================================
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"
    NOMINATIM_USER_AGENT: str = "TravelPlannerAgent/1.0"
    PLACE_SEARCH_TIMEOUT: int = 60

    # =====================================================
    # GUARDRAILS
    # =====================================================
    MIN_PROMPT_LENGTH: int = 1
    MAX_PROMPT_LENGTH: int = 100000
    MAX_CONSECUTIVE_WHITESPACE: int = 10
    MAX_REPEATED_CHARACTERS: int = 15
    MAX_EMOJI_COUNT: int = 30

    # =====================================================
    # PROMPT INJECTION
    # =====================================================
    PROMPT_INJECTION_THRESHOLD: float = 0.65
    PROMPT_INJECTION_REGEX_WEIGHT: float = 0.45
    PROMPT_INJECTION_KEYWORD_WEIGHT: float = 0.25
    PROMPT_INJECTION_EMBEDDING_WEIGHT: float = 0.30
    PROMPT_INJECTION_REGEX_EARLY_STOP: float = 0.90
    PROMPT_INJECTION_COMBINED_EARLY_STOP: float = 0.85
    PROMPT_INJECTION_SIMILARITY_THRESHOLD: float = 0.80
    PROMPT_INJECTION_EXAMPLES_FILE: str = "app/ai/prompts/prompt_injection_examples.txt"

    # =====================================================
    # MODERATION
    # =====================================================
    MODERATION_THRESHOLD: float = 0.65
    MODERATION_LOW_THRESHOLD: float = 0.30
    MODERATION_MEDIUM_THRESHOLD: float = 0.50
    MODERATION_HIGH_THRESHOLD: float = 0.75
    MODERATION_CRITICAL_THRESHOLD: float = 0.90
    MODERATION_REGEX_WEIGHT: float = 0.60
    MODERATION_KEYWORD_WEIGHT: float = 0.40
    MODERATION_REGEX_EARLY_STOP: float = 0.90
    MODERATION_COMBINED_EARLY_STOP: float = 0.80

    # Pydantic Settings Metadata Configuration
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Mengambil instance konfigurasi tunggal (Singleton) yang dioptimalkan dengan cache.
    """
    return Settings()  # pyright: ignore


# Inisialisasi instance terpusat untuk diimpor oleh modul luar
settings = get_settings()