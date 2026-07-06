from typing import Optional

from sqlalchemy.orm import Session

from app.models.currency import CurrencyHistory
from app.repositories.base_repository import BaseRepository


class CurrencyRepository(BaseRepository[CurrencyHistory]):

    def __init__(self):
        super().__init__(CurrencyHistory)

    def get_latest_rate(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
    ) -> Optional[CurrencyHistory]:

        return (
            db.query(CurrencyHistory)
            .filter(
                CurrencyHistory.base_currency == base_currency,
                CurrencyHistory.target_currency == target_currency,
            )
            .order_by(CurrencyHistory.fetched_at.desc())
            .first()
        )

    def get_history(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
    ) -> list[CurrencyHistory]:

        return (
            db.query(CurrencyHistory)
            .filter(
                CurrencyHistory.base_currency == base_currency,
                CurrencyHistory.target_currency == target_currency,
            )
            .order_by(CurrencyHistory.fetched_at.desc())
            .all()
        )