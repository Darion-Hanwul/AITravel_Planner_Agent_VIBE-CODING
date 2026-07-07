from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.currency import CurrencyHistory
from app.repositories.base_repository import BaseRepository


class CurrencyRepository(
    BaseRepository[CurrencyHistory]
):

    def __init__(self) -> None:
        super().__init__(CurrencyHistory)

    # =====================================================
    # GET LATEST EXCHANGE RATE
    # =====================================================

    def get_latest_rate(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
    ) -> Optional[CurrencyHistory]:

        stmt = (
            select(CurrencyHistory)
            .where(
                CurrencyHistory.base_currency == base_currency,
                CurrencyHistory.target_currency == target_currency,
            )
            .order_by(
                CurrencyHistory.fetched_at.desc()
            )
            .limit(1)
        )

        return db.scalar(stmt)

    # =====================================================
    # GET EXCHANGE RATE HISTORY
    # =====================================================

    def get_history(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
    ) -> list[CurrencyHistory]:

        stmt = (
            select(CurrencyHistory)
            .where(
                CurrencyHistory.base_currency == base_currency,
                CurrencyHistory.target_currency == target_currency,
            )
            .order_by(
                CurrencyHistory.fetched_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )