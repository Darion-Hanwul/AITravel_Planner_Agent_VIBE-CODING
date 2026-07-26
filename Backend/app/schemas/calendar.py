from datetime import date, time
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class CalendarEventBase(BaseModel):

    event_title: str = Field(..., min_length=2, max_length=200)

    event_date: date

    start_time: time

    end_time: time

    reminder: bool = True

    model_config = ConfigDict(
        extra="forbid",
    )

class CalendarEventCreate(CalendarEventBase):
    activity_id: UUID

class CalendarEventUpdate(BaseModel):

    event_title: str | None = None

    event_date: date | None = None

    start_time: time | None = None

    end_time: time | None = None

    reminder: bool | None = None

    model_config = ConfigDict(
        extra="forbid",
    )

class CalendarEventResponse(CalendarEventBase):

    id: UUID

    activity_id: UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )