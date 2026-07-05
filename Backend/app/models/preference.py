import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True
    )

    preferred_currency: Mapped[str] = mapped_column(String(10))

    budget_min: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    budget_max: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    favorite_country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    favorite_food: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    hotel_star: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    travel_style: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    transportation_preference: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="preferences"
    )