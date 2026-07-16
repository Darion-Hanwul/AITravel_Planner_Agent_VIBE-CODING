from __future__ import annotations

import logging

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.transportation")


class TransportationSources:
    """
    TransportationSources mengelola rujukan rute penerbangan, kereta,
    maupun moda transportasi publik lokal di destinasi tujuan (Prinsip 1).
    """

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_transport_sources(self) -> list[Source]:
        """
        Mengambil data source transportasi aktif.
        """
        logger.info("[TransportationSources] Mengambil data source transportasi aktif.")
        return self.registry.get_by_category("travel")