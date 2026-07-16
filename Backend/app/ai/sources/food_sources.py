from __future__ import annotations

import logging

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.food")


class FoodSources:
    """
    FoodSources mengelola informasi kuliner, rekomendasi tempat makan,
    serta kepatuhan diet khusus (e.g., Halal, Vegan, Alergi) (Prinsip 1).
    """

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_food_sources(self) -> list[Source]:
        """
        Mengambil data source kuliner aktif.
        """
        logger.info("[FoodSources] Mengambil data source makanan & kuliner aktif.")
        return self.registry.get_by_category("travel")