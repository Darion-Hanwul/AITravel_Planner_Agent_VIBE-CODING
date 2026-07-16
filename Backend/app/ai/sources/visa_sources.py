from __future__ import annotations

import logging

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.visa")


class VisaSources:
    """
    VisaSources mengelola sumber informasi regulasi imigrasi, paspor,
    dan travel advisory resmi antar negara (Prinsip 1, 11).
    """

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_visa_sources(self) -> list[Source]:
        """
        Mengambil sumber hukum imigrasi dan visa aktif.
        """
        logger.info("[VisaSources] Mengambil data source regulasi visa aktif.")
        return self.registry.get_by_category("visa")