from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Currency Convert Request
# ==========================================================

class CurrencyConvertRequest(BaseModel):

    base_currency: str = Field(..., min_length=3, max_length=5)

    target_currency: str = Field(..., min_length=3, max_length=5)

    amount: Decimal = Field(..., gt=0)


# ==========================================================
# Currency Convert Response
# ==========================================================

class CurrencyConvertResponse(BaseModel):

    base_currency: str

    target_currency: str

    exchange_rate: Decimal

    amount: Decimal

    converted_amount: Decimal


# ==========================================================
# Currency History
# ==========================================================

class CurrencyHistoryResponse(BaseModel):

    id: UUID

    base_currency: str

    target_currency: str

    exchange_rate: Decimal

    fetched_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )