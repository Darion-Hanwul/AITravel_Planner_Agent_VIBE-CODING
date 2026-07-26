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
from app.utils.cache import is_cache_valid
from app.models.weather import WeatherCache

from app.repositories.weather_repository import (
    WeatherRepository,
)


class WeatherTool(BaseTool):

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
    
    def _get_cached_weather(
        self,
        db: Session,
        city: str,
        country: str,
    ) -> WeatherCache | None:

        return self.weather_repository.get_latest_weather(
            db=db,
            city=city,
            country=country,
        )

    def _fetch_weather(
        self,
        city: str,
        country: str,
    ) -> tuple[str, Decimal, Decimal]:

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
    
    def run(
        self,
        **kwargs: Any,
    ) -> dict[str, object]:

        city = kwargs["city"]
        country = kwargs["country"]

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
                and is_cache_valid(
                    cache.fetched_at,
                    self.CACHE_EXPIRE_MINUTES,
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