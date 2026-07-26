from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class UserPreferenceBase(BaseModel):
    preferred_currency: str = Field(..., min_length=3, max_length=5)

    budget_min: Decimal = Field(..., ge=0)
    budget_max: Decimal = Field(..., ge=0)

    favorite_country: str | None = None
    favorite_food: str | None = None

    hotel_star: int = Field(..., ge=1, le=5)

    travel_style: str
    transportation_preference: str

class UserPreferenceCreate(UserPreferenceBase):
    pass

class UserPreferenceUpdate(BaseModel):
    preferred_currency: str | None = None

    budget_min: Decimal | None = Field(default=None, ge=0)
    budget_max: Decimal | None = Field(default=None, ge=0)

    favorite_country: str | None = None
    favorite_food: str | None = None

    hotel_star: int | None = Field(default=None, ge=1, le=5)

    travel_style: str | None = None
    transportation_preference: str | None = None

class UserPreferenceResponse(UserPreferenceBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )