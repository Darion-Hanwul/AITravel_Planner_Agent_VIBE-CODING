from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
)

from app.models.currency import CurrencyHistory

from app.repositories.currency_repository import (
    CurrencyRepository,
)

from app.schemas.currency import (
    CurrencyConvertRequest,
    CurrencyConvertResponse,
    CurrencyHistoryResponse,
)

from app.services.base_service import BaseService


class CurrencyService(BaseService):
    """
    Business logic untuk Currency.

    Bertanggung jawab terhadap:

    - Currency Conversion
    - Exchange Rate History
    - Currency Cache Management
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.currency_repository = (
            CurrencyRepository()
        )

    # ======================================================
    # PRIVATE HELPERS
    # ======================================================

    def _get_latest_rate(
        self,
        base_currency: str,
        target_currency: str,
    ) -> CurrencyHistory:
        """
        Mengambil exchange rate terbaru.
        """

        rate = (
            self.currency_repository.get_latest_rate(
                self.db,
                base_currency,
                target_currency,
            )
        )

        if rate is None:

            raise ResourceNotFoundError(
                "Exchange rate not found.",
            )

        return rate

    def _calculate_conversion(
        self,
        amount: Decimal,
        exchange_rate: Decimal,
    ) -> Decimal:
        """
        Menghitung hasil konversi currency.
        """

        return amount * exchange_rate

    def _to_history_response(
        self,
        history: CurrencyHistory,
    ) -> CurrencyHistoryResponse:
        """
        Mapping ORM ke response schema.
        """

        return CurrencyHistoryResponse.model_validate(
            history,
        )

    # ======================================================
    # PUBLIC METHODS
    # ======================================================

    def convert_currency(
        self,
        data: CurrencyConvertRequest,
    ) -> CurrencyConvertResponse:
        """
        Melakukan currency conversion
        menggunakan exchange rate terbaru.
        """

        rate = self._get_latest_rate(
            data.base_currency,
            data.target_currency,
        )

        converted_amount = (
            self._calculate_conversion(
                data.amount,
                rate.exchange_rate,
            )
        )

        return CurrencyConvertResponse(
            base_currency=data.base_currency,
            target_currency=data.target_currency,
            exchange_rate=rate.exchange_rate,
            amount=data.amount,
            converted_amount=converted_amount,
        )

    def save_exchange_rate(
        self,
        base_currency: str,
        target_currency: str,
        exchange_rate: Decimal,
    ) -> CurrencyHistoryResponse:
        """
        Menyimpan exchange rate baru.

        Data biasanya berasal dari
        Currency Tool / External API.
        """

        currency_history = CurrencyHistory(
            base_currency=base_currency,
            target_currency=target_currency,
            exchange_rate=exchange_rate,
        )

        try:

            self.currency_repository.create(
                self.db,
                currency_history,
            )

            self.commit()

            self.refresh(
                currency_history,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_history_response(
            currency_history,
        )

    def get_history(
        self,
        base_currency: str,
        target_currency: str,
    ) -> list[CurrencyHistoryResponse]:
        """
        Mengambil history exchange rate.
        """

        histories = (
            self.currency_repository.get_history(
                self.db,
                base_currency,
                target_currency,
            )
        )

        return [
            self._to_history_response(
                history,
            )
            for history in histories
        ]