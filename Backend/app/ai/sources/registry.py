from app.ai.sources.source import Source
from app.ai.sources.travel_sources import (
    TRAVEL_SOURCES,
)


class SourceRegistry:
    """
    Registry seluruh knowledge source.
    """

    SOURCES: list[Source] = [
        *TRAVEL_SOURCES,
    ]

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    @classmethod
    def get_all(
        cls,
    ) -> list[Source]:

        return [
            source
            for source in cls.SOURCES
            if source.enabled
        ]

    @classmethod
    def get_by_category(
        cls,
        category: str,
    ) -> list[Source]:

        return [
            source
            for source in cls.get_all()
            if source.category.lower()
            == category.lower()
        ]

    @classmethod
    def get_by_name(
        cls,
        name: str,
    ) -> Source | None:

        for source in cls.get_all():

            if source.name.lower() == name.lower():

                return source

        return None