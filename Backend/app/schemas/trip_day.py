from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.activity import ActivityResponse

class TripDayBase(BaseModel):

    day_number: int = Field(..., ge=1)

    title: str = Field(..., min_length=2, max_length=150)

    description: str | None = None


class TripDayCreate(TripDayBase):
    pass


class TripDayUpdate(BaseModel):

    day_number: int | None = Field(default=None, ge=1)

    title: str | None = None

    description: str | None = None


class TripDayResponse(TripDayBase):

    id: UUID

    trip_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class TripDayDetailResponse(TripDayResponse):

    activities: list[ActivityResponse] = []