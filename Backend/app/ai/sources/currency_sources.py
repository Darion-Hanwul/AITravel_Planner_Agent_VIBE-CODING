from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.currency")


class CurrencySources:

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:

        self.registry = registry

    def get_active_currency_sources(self) -> list[Source]:

        logger.info("[CurrencySources] Mengambil data source finansial aktif.")
        return self.registry.get_by_category("currency")

    def get_currency_fallback(self, source_currency: str, target_currency: str) -> dict[str, Any]:

        logger.debug(f"[CurrencySources] Membuat data fallback kurs {source_currency} ke {target_currency}.")
        return {
            "source": source_currency.upper(),
            "target": target_currency.upper(),
            "rate": 1.0,
            "note": "Menggunakan nilai baseline 1:1 karena kendala jaringan koneksi."
        }