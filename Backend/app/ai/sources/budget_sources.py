from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.budget")


class BudgetSources:
    """
    BudgetSources bertanggung jawab mengelola metadata rujukan biaya, 
    indeks harga hidup, dan alokasi dana perjalanan (Prinsip 1, 11).

    Responsibility
    --------------
    - Mengambil metadata source kategori 'travel' atau 'currency' untuk analisis finansial.
    - Menyediakan batas atas dan bawah (cost baseline) aman sebagai guardrail anggaran.
    """

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_budget_sources(self) -> list[Source]:
        """
        Mengambil semua data source finansial dan travel aktif yang relevan dengan anggaran.
        """
        logger.info("[BudgetSources] Mengambil data source anggaran aktif.")
        return [
            source for source in self.registry.get_all()
            if source.category in ("travel", "currency")
        ]

    def get_cost_allowance_baseline(self, destination: str, duration_days: int) -> dict[str, Any]:
        """
        Menyediakan kalkulasi baseline biaya harian minimum (fail-safe) 
        jika data biaya spesifik gagal ditarik dari Vector Database (Prinsip 10).

        Args:
            destination: Nama negara/kota tujuan perjalanan.
            duration_days: Durasi total liburan dalam hitungan hari.

        Returns:
            dict[str, Any]: Batas alokasi biaya acuan dasar dalam USD.
        """
        logger.debug(f"[BudgetSources] Menghitung baseline dana darurat untuk {destination} ({duration_days} hari).")
        
        # Angka referensi global dasar per hari ($50 USD/hari untuk akomodasi + makan standar)
        base_rate_per_day = 50.0
        minimum_total = base_rate_per_day * duration_days

        return {
            "destination": destination,
            "duration_days": duration_days,
            "suggested_daily_allowance_usd": base_rate_per_day,
            "minimum_safe_budget_usd": minimum_total,
            "note": "Perhitungan menggunakan baseline aman terintegrasi (fail-safe global index)."
        }