import uuid
from decimal import Decimal
from datetime import time

from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    trip_day_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trip_days.id", ondelete="CASCADE")
    )

    place_name: Mapped[str] = mapped_column(
        String(255)
    )

    category: Mapped[str] = mapped_column(
        String(100)
    )

    start_time: Mapped[time] = mapped_column(
        Time
    )

    end_time: Mapped[time] = mapped_column(
        Time
    )

    estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    latitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7)
    )

    longitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7)
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    trip_day = relationship(
        "TripDay",
        back_populates="activities"
    )

    calendar_event = relationship(
        "CalendarEvent",
        back_populates="activity",
        cascade="all, delete-orphan",
        uselist=False
    )