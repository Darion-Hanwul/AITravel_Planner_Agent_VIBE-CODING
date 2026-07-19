from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.ai.tools.base_tool import BaseTool
from app.config.settings import settings
from app.core.logger import logger
from app.db.session import SessionLocal
from app.utils.cache import is_cache_valid

from app.models.currency import CurrencyHistory
from app.repositories.currency_repository import (
    CurrencyRepository,
)


class CurrencyTool(BaseTool):
    """
    Currency Tool.

    Responsibility
    --------------

    - Mengambil nilai tukar mata uang dari
      ExchangeRate API.
    - Menyimpan exchange rate ke database.
    - Menggunakan cache apabila masih valid.
    - Menghitung hasil konversi mata uang.
    - Logging seluruh proses.

    Tidak bertanggung jawab terhadap:

    - Prompt Engineering
    - LangGraph
    - Memory
    - Tool Registry
    - LLM
    """

    NAME = "currency"

    DESCRIPTION = (
        "Convert money between currencies "
        "using latest exchange rates."
    )

    DEFAULT_TIMEOUT = 30

    CACHE_EXPIRE_MINUTES = (
        settings.CURRENCY_CACHE_EXPIRE_MINUTES
    )

    def __init__(
        self,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        enabled: bool = True,
    ) -> None:
        """
        Initialize Currency Tool.
        """

        super().__init__(
            enabled=enabled,
        )

        self.timeout = timeout

        self.base_url = (
            settings.EXCHANGERATE_BASE_URL
        )

        self.api_key = (
            settings.EXCHANGERATE_API_KEY
        )

        self.http = httpx.Client(
            timeout=self.timeout,
        )

        self.currency_repository = (
            CurrencyRepository()
        )

    def __del__(self) -> None:
        """
        Menutup HTTP client ketika object
        dihancurkan.
        """

        try:
            self.http.close()
        except Exception:
            pass

    # =====================================================
    # METADATA
    # =====================================================

    @property
    def name(
        self,
    ) -> str:

        return self.NAME

    @property
    def description(
        self,
    ) -> str:

        return self.DESCRIPTION

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _normalize_currency(
        self,
        currency: str,
    ) -> str:
        """
        Normalisasi dan validasi kode mata uang
        berdasarkan standar ISO 4217.
        """

        currency = currency.strip().upper()

        if len(currency) != 3 or not currency.isalpha():
            raise ValueError(
                "Currency code must be ISO 4217 (3 letters)."
            )

        return currency

    def _get_cached_rate(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
    ) -> CurrencyHistory | None:
        """
        Mengambil exchange rate terbaru
        dari database.
        """

        return self.currency_repository.get_latest_rate(
            db=db,
            base_currency=base_currency,
            target_currency=target_currency,
        )
    
    def _fetch_exchange_rate(
        self,
        base_currency: str,
        target_currency: str,
    ) -> Decimal:
        """
        Mengambil exchange rate terbaru dari
        ExchangeRate API.

        Args:
            base_currency:
                Mata uang asal.

            target_currency:
                Mata uang tujuan.

        Returns:
            Exchange rate terbaru.

        Raises:
            RuntimeError:
                Apabila request ke API gagal.
        """

        logger.info(
            "Fetching exchange rate from "
            "ExchangeRate API "
            f"({base_currency} -> {target_currency})"
        )

        try:

            response = self.http.get(
                (
                    f"{self.base_url}/"
                    f"{self.api_key}/pair/"
                    f"{base_currency}/"
                    f"{target_currency}"
                ),
            )

            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":

                raise RuntimeError(
                    data.get(
                        "error-type",
                        "Unknown ExchangeRate API error.",
                    )
                )

            exchange_rate = Decimal(
                str(
                    data["conversion_rate"]
                )
            )

            logger.info(
                "Exchange rate fetched successfully "
                f"({base_currency} -> {target_currency})"
            )

            return exchange_rate

        except httpx.HTTPError as exc:

            logger.exception(
                "HTTP error while requesting "
                "ExchangeRate API."
            )

            raise RuntimeError(
                "Unable to fetch exchange rate."
            ) from exc

        except KeyError as exc:

            logger.exception(
                "Invalid ExchangeRate API response."
            )

            raise RuntimeError(
                "Invalid exchange rate response."
            ) from exc

        except Exception as exc:

            logger.exception(
                "Unexpected error while "
                "fetching exchange rate."
            )

            raise RuntimeError(
                "Unable to fetch exchange rate."
            ) from exc

    def _calculate_conversion(
        self,
        amount: Decimal,
        exchange_rate: Decimal,
    ) -> Decimal:
        """
        Menghitung hasil konversi mata uang.

        Returns:
            Nilai hasil konversi.
        """

        return (
            amount * exchange_rate
        ).quantize(
            Decimal("0.000001")
        )

    def _save_cache(
        self,
        db: Session,
        base_currency: str,
        target_currency: str,
        exchange_rate: Decimal,
    ) -> CurrencyHistory:
        """
        Menyimpan exchange rate terbaru
        ke database.

        Returns:
            CurrencyHistory yang telah
            berhasil disimpan.
        """

        cache = CurrencyHistory(
            base_currency=base_currency,
            target_currency=target_currency,
            exchange_rate=exchange_rate,
        )

        self.currency_repository.create(
            db,
            cache,
        )

        db.commit()

        db.refresh(
            cache,
        )

        logger.info(
            "Currency cache saved "
            f"({base_currency} -> {target_currency})"
        )

        return cache
    
    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def run(
        self,
        **kwargs: Any,
    ) -> dict[str, object]:
        """
        Mengambil nilai tukar mata uang dan
        melakukan konversi.

        Workflow

            1. Normalisasi currency code.
            2. Validasi amount.
            3. Cek cache database.
            4. Jika cache masih valid,
               gunakan cache.
            5. Jika cache tidak valid,
               ambil dari ExchangeRate API.
            6. Simpan cache baru.
            7. Hitung hasil konversi.
            8. Return hasil.
        """

        base_currency = self._normalize_currency(
            kwargs["base_currency"],
        )

        target_currency = self._normalize_currency(
            kwargs["target_currency"],
        )

        amount = Decimal(
            str(
                kwargs["amount"],
            )
        )

        if amount <= Decimal("0"):

            raise ValueError(
                "Amount must be greater than zero."
            )

        logger.info(
            "CurrencyTool started "
            f"({base_currency} -> {target_currency})"
        )

        db = SessionLocal()

        try:

            cache = self._get_cached_rate(
                db=db,
                base_currency=base_currency,
                target_currency=target_currency,
            )

            if (
                cache is not None
                and is_cache_valid(
                    cache.fetched_at,
                    self.CACHE_EXPIRE_MINUTES,
                )
            ):

                logger.info(
                    "Using cached exchange rate "
                    f"({base_currency} -> "
                    f"{target_currency})"
                )

                converted_amount = (
                    self._calculate_conversion(
                        amount=amount,
                        exchange_rate=cache.exchange_rate,
                    )
                )

                return {
                    "source": "cache",
                    "base_currency": (
                        cache.base_currency
                    ),
                    "target_currency": (
                        cache.target_currency
                    ),
                    "exchange_rate": float(
                        cache.exchange_rate,
                    ),
                    "amount": float(
                        amount,
                    ),
                    "converted_amount": float(
                        converted_amount,
                    ),
                    "fetched_at": (
                        cache.fetched_at.isoformat()
                    ),
                }
            
            exchange_rate = self._fetch_exchange_rate(
                base_currency=base_currency,
                target_currency=target_currency,
            )

            cache = self._save_cache(
                db=db,
                base_currency=base_currency,
                target_currency=target_currency,
                exchange_rate=exchange_rate,
            )

            converted_amount = (
                self._calculate_conversion(
                    amount=amount,
                    exchange_rate=cache.exchange_rate,
                )
            )

            logger.info(
                "Fresh exchange rate saved "
                f"({base_currency} -> "
                f"{target_currency})"
            )

            return {
                "source": "api",
                "base_currency": (
                    cache.base_currency
                ),
                "target_currency": (
                    cache.target_currency
                ),
                "exchange_rate": float(
                    cache.exchange_rate,
                ),
                "amount": float(
                    amount,
                ),
                "converted_amount": float(
                    converted_amount,
                ),
                "fetched_at": (
                    cache.fetched_at.isoformat()
                ),
            }
        
        except Exception:

            db.rollback()

            logger.exception(
                "CurrencyTool execution failed."
            )

            raise

        finally:

            db.close()

            logger.info(
                "CurrencyTool finished."
            )