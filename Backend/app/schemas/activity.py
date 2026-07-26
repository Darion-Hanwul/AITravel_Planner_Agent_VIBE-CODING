from datetime import time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class ActivityBase(BaseModel):

    place_name: str = Field(..., min_length=2, max_length=200)

    category: str = Field(..., min_length=2, max_length=100)

    start_time: time

    end_time: time

    estimated_cost: Decimal = Field(..., ge=0)

    latitude: Decimal | None = None

    longitude: Decimal | None = None

    notes: str | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):

    place_name: str | None = None

    category: str | None = None

    start_time: time | None = None

    end_time: time | None = None

    estimated_cost: Decimal | None = Field(default=None, ge=0)

    latitude: Decimal | None = None

    longitude: Decimal | None = None

    notes: str | None = None

class ActivityResponse(ActivityBase):

    id: UUID

    trip_day_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )