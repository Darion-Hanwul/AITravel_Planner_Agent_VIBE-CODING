from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.trip_day import TripDayDetailResponse


# ==========================================================
# Base
# ==========================================================

class TripBase(BaseModel):

    title: str = Field(..., min_length=3, max_length=200)

    destination: str = Field(..., min_length=2, max_length=150)

    start_date: date

    end_date: date

    budget: Decimal = Field(..., ge=0)

    total_estimated_cost: Decimal = Field(..., ge=0)

    status: str


# ==========================================================
# Create
# ==========================================================

class TripCreate(TripBase):
    pass


# ==========================================================
# Update
# ==========================================================

class TripUpdate(BaseModel):

    title: str | None = None

    destination: str | None = None

    start_date: date | None = None

    end_date: date | None = None

    budget: Decimal | None = Field(default=None, ge=0)

    total_estimated_cost: Decimal | None = Field(default=None, ge=0)

    status: str | None = None


# ==========================================================
# Response
# ==========================================================

class TripResponse(TripBase):

    id: UUID

    user_id: UUID

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# Detail Response
# ==========================================================

class TripDetailResponse(TripResponse):

    trip_days: list[TripDayDetailResponse] = []