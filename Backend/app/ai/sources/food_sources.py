from __future__ import annotations

import logging

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.food")


class FoodSources:

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_food_sources(self) -> list[Source]:

        logger.info("[FoodSources] Mengambil data source makanan & kuliner aktif.")
        return self.registry.get_by_category("travel")