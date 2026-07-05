import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class SavedPlace(Base):
    __tablename__ = "saved_places"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    name: Mapped[str] = mapped_column(
        String(255)
    )

    country: Mapped[str] = mapped_column(
        String(100)
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    latitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7)
    )

    longitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 7)
    )

    category: Mapped[str] = mapped_column(
        String(100)
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="saved_places"
    )