from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.budget")


class BudgetSources:

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:

        self.registry = registry

    def get_active_budget_sources(self) -> list[Source]:

        logger.info("[BudgetSources] Mengambil data source anggaran aktif.")
        return [
            source for source in self.registry.get_all()
            if source.category in ("travel", "currency")
        ]

    def get_cost_allowance_baseline(self, destination: str, duration_days: int) -> dict[str, Any]:

        logger.debug(f"[BudgetSources] Menghitung baseline dana darurat untuk {destination} ({duration_days} hari).")
        
        base_rate_per_day = 50.0
        minimum_total = base_rate_per_day * duration_days

        return {
            "destination": destination,
            "duration_days": duration_days,
            "suggested_daily_allowance_usd": base_rate_per_day,
            "minimum_safe_budget_usd": minimum_total,
            "note": "Perhitungan menggunakan baseline aman terintegrasi (fail-safe global index)."
        }