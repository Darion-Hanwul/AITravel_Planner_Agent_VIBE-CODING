from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weather import WeatherCache
from app.repositories.base_repository import BaseRepository


class WeatherRepository(
    BaseRepository[WeatherCache]
):

    def __init__(self) -> None:
        super().__init__(WeatherCache)

    def get_latest_weather(
        self,
        db: Session,
        city: str,
        country: str,
    ) -> Optional[WeatherCache]:

        stmt = (
            select(WeatherCache)
            .where(
                WeatherCache.city == city,
                WeatherCache.country == country,
            )
            .order_by(
                WeatherCache.fetched_at.desc()
            )
            .limit(1)
        )

        return db.scalar(stmt)

    def delete_cache(
        self,
        db: Session,
        cache: WeatherCache,
    ) -> None:

        self.delete(
            db,
            cache,
        )