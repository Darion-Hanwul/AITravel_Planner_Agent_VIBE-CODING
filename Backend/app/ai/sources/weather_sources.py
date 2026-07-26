from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.weather")


class WeatherSources:

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:

        self.registry = registry

    def get_active_weather_sources(self) -> list[Source]:

        logger.info("[WeatherSources] Mengambil data source cuaca aktif.")
        return self.registry.get_by_category("weather")

    def get_weather_context_stub(self, destination: str) -> dict[str, Any]:

        logger.debug(f"[WeatherSources] Membuat mock/stub cuaca untuk {destination}.")

        return {
            "location": destination,
            "condition": "Informasi perkiraan cuaca lokal tersedia di dokumen referensi RAG.",
            "status": "UNKNOWN"
        }