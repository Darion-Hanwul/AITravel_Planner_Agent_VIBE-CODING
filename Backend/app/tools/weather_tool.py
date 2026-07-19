"""
Weather Tool.

Tool layer untuk mengakses WeatherService.

Responsibility
--------------
- Validasi request.
- Meneruskan request ke WeatherService.
- Mengembalikan WeatherResponse.

Tidak bertanggung jawab terhadap:
- HTTP Request OpenWeather API
- Cache Database
- Repository
- Business Logic
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.schemas.weather import (
    WeatherRequest,
    WeatherResponse,
)
from app.services.weather_service import WeatherService


class WeatherTool:
    """
    Wrapper untuk WeatherService.

    Digunakan oleh API Layer maupun AI Layer apabila
    membutuhkan informasi cuaca melalui business layer.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.weather_service = WeatherService(
            db,
        )

    def execute(
        self,
        city: str,
        country: str,
    ) -> WeatherResponse:
        """
        Mengambil informasi cuaca.

        Args:
            city:
                Nama kota.

            country:
                Kode negara (ISO-3166 Alpha-2).

        Returns:
            WeatherResponse
        """

        request = WeatherRequest(
            city=city,
            country=country,
        )

        return self.weather_service.get_weather(
            request,
        )

    def save(
        self,
        city: str,
        country: str,
        weather: str,
        temperature,
        humidity,
    ) -> WeatherResponse:
        """
        Menyimpan weather cache baru.
        """

        return self.weather_service.save_weather(
            city=city,
            country=country,
            weather=weather,
            temperature=temperature,
            humidity=humidity,
        )