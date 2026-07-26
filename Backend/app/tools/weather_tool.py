import uuid
import requests
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.db.models import WeatherCache

class WeatherTool:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.api_key = "a03b64fcb99d7376f1c586d210fe491b"

    def get_weather(self, city: str, country: str) -> dict:
        url = f"{self.base_url}/weather"
        params = {"q": f"{city},{country}", "appid": self.api_key, "units": "metric"}
        response = requests.get(url, params=params).json()
        if response.get("cod") == 200:
            weather_data = {
                "weather": response["weather"][0]["main"],
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"]
            }
            cache = WeatherCache(
                id=uuid.uuid4(),
                city=city,
                country=country,
                weather=weather_data["weather"],
                temperature=Decimal(str(weather_data["temperature"])),
                humidity=Decimal(str(weather_data["humidity"])),
                fetched_at=datetime.utcnow()
            )
            self.db.add(cache)
            self.db.commit()
            return weather_data
        return {"error": "Weather data fetch failed"}