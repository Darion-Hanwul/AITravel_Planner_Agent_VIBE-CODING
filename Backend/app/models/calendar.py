import uuid

from datetime import date
from datetime import time

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="CASCADE"),
        unique=True
    )

    event_title: Mapped[str] = mapped_column(
        String(255)
    )

    event_date: Mapped[date] = mapped_column(
        Date
    )

    start_time: Mapped[time] = mapped_column(
        Time
    )

    end_time: Mapped[time] = mapped_column(
        Time
    )

    reminder: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    activity = relationship(
        "Activity",
        back_populates="calendar_event"
    )