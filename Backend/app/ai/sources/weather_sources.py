from __future__ import annotations

import logging
from typing import Any

from app.ai.sources.registry import SourceRegistry
from app.ai.sources.source import Source

logger = logging.getLogger("app.ai.sources.weather")


class WeatherSources:
    """
    WeatherSources bertanggung jawab menyediakan konfigurasi dan akses data 
    terkait informasi cuaca destinasi (Prinsip 1, 11).

    Responsibility
    --------------
    - Mengambil metadata source kategori 'weather' dari SourceRegistry.
    - Menyediakan antarmuka data cuaca terisolasi yang akan digunakan oleh WeatherTool.

    Tidak bertanggung jawab terhadap:
    - Logika komputasi LLM (tugas Research/Schedule Agent).
    - Proses pemanggilan HTTP client mentah (tugas Base/WebLoader).
    """

    def __init__(self, registry: type[SourceRegistry] = SourceRegistry) -> None:
        self.registry = registry

    def get_active_weather_sources(self) -> list[Source]:
        """
        Mengambil semua data source cuaca yang berstatus aktif dari registry.

        Returns:
            list[Source]: Koleksi objek Source untuk domain cuaca.
        """
        logger.info("[WeatherSources] Mengambil data source cuaca aktif.")
        return self.registry.get_by_category("weather")

    def get_weather_context_stub(self, destination: str) -> dict[str, Any]:
        """
        Menyediakan data fallback/context terstruktur untuk cuaca destinasi (Prinsip 10).
        Fungsi ini menjamin alat bantu tetap mengembalikan struktur data yang aman 
        jika data live belum terindeks di VDB (Vector Database).

        Args:
            destination: Nama lokasi target percarian cuaca.

        Returns:
            dict[str, Any]: Informasi cuaca aman (fallback data).
        """
        logger.debug(f"[WeatherSources] Membuat mock/stub cuaca untuk {destination}.")
        # Mengembalikan baseline data aman (fail-safe data structure)
        return {
            "location": destination,
            "condition": "Informasi perkiraan cuaca lokal tersedia di dokumen referensi RAG.",
            "status": "UNKNOWN"
        }