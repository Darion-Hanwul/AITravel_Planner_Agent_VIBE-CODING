from typing import Optional

from sqlalchemy.orm import Session

from app.models.weather import WeatherCache
from app.repositories.base_repository import BaseRepository


class WeatherRepository(BaseRepository[WeatherCache]):

    def __init__(self):
        super().__init__(WeatherCache)

    def get_latest_weather(
        self,
        db: Session,
        city: str,
        country: str,
    ) -> Optional[WeatherCache]:

        return (
            db.query(WeatherCache)
            .filter(
                WeatherCache.city == city,
                WeatherCache.country == country,
            )
            .order_by(WeatherCache.fetched_at.desc())
            .first()
        )

    def delete_cache(
        self,
        db: Session,
        cache: WeatherCache,
    ) -> None:

        db.delete(cache)
        db.commit()