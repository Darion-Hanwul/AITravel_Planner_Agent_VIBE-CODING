import uuid
from datetime import date
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    destination: Mapped[str] = mapped_column(
        String(255)
    )

    start_date: Mapped[date] = mapped_column(
        Date
    )

    end_date: Mapped[date] = mapped_column(
        Date
    )

    budget: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    total_estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="planning"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
        "User",
        back_populates="trips"
    )

    trip_days = relationship(
        "TripDay",
        back_populates="trip",
        cascade="all, delete-orphan"
    )

    tool_logs = relationship(
        "ToolLog",
        back_populates="trip",
        cascade="all, delete-orphan"
    )