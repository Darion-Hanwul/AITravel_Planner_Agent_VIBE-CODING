from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class WeatherRequest(BaseModel):

    city: str = Field(..., min_length=2)

    country: str = Field(..., min_length=2)

class WeatherResponse(BaseModel):

    id: UUID

    city: str

    country: str

    weather: str

    temperature: Decimal

    humidity: Decimal

    fetched_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )