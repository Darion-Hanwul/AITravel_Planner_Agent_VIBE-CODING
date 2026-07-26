from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
)

from app.models.weather import WeatherCache

from app.repositories.weather_repository import (
    WeatherRepository,
)

from app.schemas.weather import (
    WeatherRequest,
    WeatherResponse,
)

from app.services.base_service import BaseService


class WeatherService(BaseService):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.weather_repository = (
            WeatherRepository()
        )

    def _get_weather_cache(
        self,
        city: str,
        country: str,
    ) -> WeatherCache:

        weather = (
            self.weather_repository.get_latest_weather(
                self.db,
                city,
                country,
            )
        )

        if weather is None:

            raise ResourceNotFoundError(
                "Weather cache not found.",
            )

        return weather

    def _to_response(
        self,
        weather: WeatherCache,
    ) -> WeatherResponse:

        return WeatherResponse.model_validate(
            weather,
        )

    def get_weather(
        self,
        data: WeatherRequest,
    ) -> WeatherResponse:

        weather = self._get_weather_cache(
            data.city,
            data.country,
        )

        return self._to_response(
            weather,
        )

    def save_weather(
        self,
        city: str,
        country: str,
        weather: str,
        temperature,
        humidity,
    ) -> WeatherResponse:

        weather_cache = WeatherCache(
            city=city,
            country=country,
            weather=weather,
            temperature=temperature,
            humidity=humidity,
        )

        try:

            self.weather_repository.create(
                self.db,
                weather_cache,
            )

            self.commit()

            self.refresh(
                weather_cache,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            weather_cache,
        )

    def delete_weather_cache(
        self,
        weather_id: UUID,
    ) -> None:

        weather = (
            self.weather_repository.get_by_id(
                self.db,
                weather_id,
            )
        )

        if weather is None:

            raise ResourceNotFoundError(
                "Weather cache not found.",
            )

        try:

            self.weather_repository.delete_cache(
                self.db,
                weather,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise