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


class CurrencyHistory(Base):
    __tablename__ = "currency_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    base_currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    target_currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    exchange_rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 6),
        nullable=False
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )