from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.config.settings import settings
from app.core.logger import logger
from app.db.session import SessionLocal

from app.models.weather import WeatherCache
from app.repositories.weather_repository import (
    WeatherRepository,
)


class WeatherTool(BaseTool):
    """
    Weather Tool.

    Bertanggung jawab terhadap:

    - Mengambil data cuaca dari OpenWeather API
    - Melakukan cache ke database
    - Mengambil cache apabila masih valid
    - Logging proses tool

    Tidak bertanggung jawab terhadap:

    - Prompt
    - RAG
    - LangGraph
    - Tool Registry
    """

    NAME = "weather"

    DESCRIPTION = (
        "Get current weather information "
        "for a city."
    )

    DEFAULT_TIMEOUT = 30

    CACHE_EXPIRE_MINUTES = (
        settings.WEATHER_CACHE_EXPIRE_MINUTES
    )

    def __init__(
        self,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        enabled: bool = True,
    ) -> None:
        """
        Initialize Weather Tool.
        """

        super().__init__(
            enabled=enabled,
        )

        self.timeout = timeout

        self.base_url = (
            settings.OPENWEATHER_BASE_URL
        )

        self.api_key = (
            settings.OPENWEATHER_API_KEY
        )

        self.http = httpx.Client(
            timeout=self.timeout,
        )

        self.weather_repository = (
            WeatherRepository()
        )

    # =====================================================
    # METADATA
    # =====================================================

    @property
    def name(
        self,
    ) -> str:

        return self.NAME

    @property
    def description(
        self,
    ) -> str:

        return self.DESCRIPTION
    
    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _get_cached_weather(
        self,
        db: Session,
        city: str,
        country: str,
    ) -> WeatherCache | None:
        """
        Mengambil weather cache terbaru berdasarkan
        kota dan negara.

        Returns:
            WeatherCache jika tersedia,
            None apabila belum ada cache.
        """

        return self.weather_repository.get_latest_weather(
            db=db,
            city=city,
            country=country,
        )

    def _is_cache_valid(
        self,
        weather: WeatherCache,
    ) -> bool:
        """
        Mengecek apakah weather cache masih valid.

        Cache dianggap valid apabila umur cache
        belum melebihi WEATHER_CACHE_EXPIRE_MINUTES.
        """

        if weather.fetched_at is None:
            return False

        expire_time = weather.fetched_at + timedelta(
            minutes=self.CACHE_EXPIRE_MINUTES,
        )

        return datetime.utcnow() < expire_time
    
    def _fetch_weather(
        self,
        city: str,
        country: str,
    ) -> tuple[str, Decimal, Decimal]:
        """
        Mengambil data cuaca terbaru dari
        OpenWeather API.

        Returns:
            (
                weather, temperature, humidity,
            )

        Raises:
            RuntimeError: Jika request API gagal.
        """

        logger.info(
            f"Fetching weather from OpenWeather "
            f"({city}, {country})"
        )

        try:

            response = self.http.get(
                f"{self.base_url}/weather",
                params={
                    "q": f"{city},{country}",
                    "appid": self.api_key,
                    "units": "metric",
                },
            )

            response.raise_for_status()

            data = response.json()

            weather = data["weather"][0]["main"]

            temperature = Decimal(
                str(
                    data["main"]["temp"]
                )
            )

            humidity = Decimal(
                str(
                    data["main"]["humidity"]
                )
            )

            logger.info(
                f"Weather fetched successfully "
                f"({city}, {country})"
            )

            return (
                weather,
                temperature,
                humidity,
            )

        except Exception as exc:

            logger.exception(
                "Failed fetching weather "
                "from OpenWeather."
            )

            raise RuntimeError(
                "Unable to fetch weather."
            ) from exc

    def _save_cache(
        self,
        db: Session,
        city: str,
        country: str,
        weather: str,
        temperature: Decimal,
        humidity: Decimal,
    ) -> WeatherCache:
        """
        Menyimpan weather baru ke database.

        Returns: WeatherCache yang telah disimpan.
        """

        cache = WeatherCache(
            city=city,
            country=country,
            weather=weather,
            temperature=temperature,
            humidity=humidity,
        )

        self.weather_repository.create(
            db,
            cache,
        )

        db.commit()

        db.refresh(
            cache,
        )

        logger.info(
            f"Weather cache saved "
            f"({city}, {country})"
        )

        return cache
    
        # =====================================================
        # PUBLIC METHODS
        # =====================================================

    def run(
        self,
        **kwargs: Any,
    ) -> dict[str, object]:

        city = kwargs["city"]
        country = kwargs["country"]

        """
        Mengambil informasi cuaca.

        Workflow:

            1. Cek cache.
            2. Jika cache masih valid, gunakan cache.
            3. Jika tidak, ambil dari OpenWeather.
            4. Simpan cache baru.
            5. Return hasil.

        Args:
            city: Nama kota.

            country:
                Kode negara (ISO 3166-1 Alpha-2),
                misalnya: ID, JP, SG, AU

        Returns: Dictionary hasil cuaca.
        """

        logger.info(
            f"WeatherTool started "
            f"({city}, {country})"
        )

        db = SessionLocal()

        try:

            cache = self._get_cached_weather(
                db=db,
                city=city,
                country=country,
            )

            if (
                cache is not None
                and self._is_cache_valid(
                    cache,
                )
            ):

                logger.info(
                    f"Using cached weather "
                    f"({city}, {country})"
                )

                return {
                    "source": "cache",
                    "city": cache.city,
                    "country": cache.country,
                    "weather": cache.weather,
                    "temperature": float(
                        cache.temperature,
                    ),
                    "humidity": float(
                        cache.humidity,
                    ),
                    "fetched_at": (
                        cache.fetched_at.isoformat()
                    ),
                }

            (
                weather,
                temperature,
                humidity,
            ) = self._fetch_weather(
                city=city,
                country=country,
            )

            cache = self._save_cache(
                db=db,
                city=city,
                country=country,
                weather=weather,
                temperature=temperature,
                humidity=humidity,
            )

            logger.info(
                f"Fresh weather saved "
                f"({city}, {country})"
            )

            return {
                "source": "api",
                "city": cache.city,
                "country": cache.country,
                "weather": cache.weather,
                "temperature": float(
                    cache.temperature,
                ),
                "humidity": float(
                    cache.humidity,
                ),
                "fetched_at": (
                    cache.fetched_at.isoformat()
                ),
            }

        except Exception:

            db.rollback()

            logger.exception(
                "WeatherTool execution failed."
            )

            raise

        finally:

            db.close()

            logger.info(
                "WeatherTool finished."
            )