from __future__ import annotations

from app.ai.sources.source import Source
from app.ai.sources.travel_sources import TRAVEL_SOURCES


class SourceRegistry:

    SOURCES: list[Source] = [
        *TRAVEL_SOURCES,
    ]

    @classmethod
    def get_all(cls) -> list[Source]:

        return [
            source
            for source in cls.SOURCES
            if source.enabled
        ]

    @classmethod
    def get_by_category(cls, category: str) -> list[Source]:

        target_category = category.lower()
        return [
            source
            for source in cls.get_all()
            if source.category.lower() == target_category
        ]

    @classmethod
    def get_by_name(cls, name: str) -> Source | None:

        target_name = name.lower()
        for source in cls.get_all():
            if source.name.lower() == target_name:
                return source
        return None