from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.accommodation")


class AccomodationSources:

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:

        self.registry = registry

    def get_active_accommodation_sources(self) -> list[Source]:

        logger.info("[AccomodationSources] Mengambil data source akomodasi aktif.")
        return self.registry.get_by_category("travel")

    def get_default_pricing_tier(self, budget_tier: str) -> dict[str, Any]:

        tiers = {
            "backpacker": {"estimated_cost_usd": 15, "type": "Hostel/Shared Room"},
            "moderate": {"estimated_cost_usd": 50, "type": "Standard Hotel Room"},
            "luxury": {"estimated_cost_usd": 200, "type": "Resort/Luxury Hotel"}
        }
        return tiers.get(budget_tier.lower(), tiers["moderate"])