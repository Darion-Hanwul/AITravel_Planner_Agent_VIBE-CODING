import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class WeatherCache(Base):
    __tablename__ = "weather_cache"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    weather: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    temperature: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    humidity: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )