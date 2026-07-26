from __future__ import annotations

from decimal import Decimal
from typing import Any

import httpx

from app.ai.tools.base_tool import BaseTool
from app.config.settings import settings
from app.core.logger import logger

from app.schemas.saved_place import (
    ForwardGeocodeResult,
    PlaceSearchResult,
    ReverseGeocodeResult,
)


class PlaceSearchTool(BaseTool):

    NAME = "place_search"

    DESCRIPTION = (
        "Search places and perform "
        "forward/reverse geocoding "
        "using OpenStreetMap Nominatim."
    )

    ACTION_SEARCH = "search"

    ACTION_FORWARD_GEOCODE = (
        "forward_geocode"
    )

    ACTION_REVERSE_GEOCODE = (
        "reverse_geocode"
    )

    DEFAULT_TIMEOUT = (
        settings.PLACE_SEARCH_TIMEOUT
    )

    def __init__(
        self,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        enabled: bool = True,
    ) -> None:
        """
        Initialize PlaceSearchTool.
        """

        super().__init__(
            enabled=enabled,
        )

        self.timeout = timeout

        self.base_url = (
            settings.NOMINATIM_BASE_URL
        )

        self.user_agent = (
            settings.NOMINATIM_USER_AGENT
        )

        self.http = httpx.Client(
            timeout=self.timeout,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "application/json",
            },
        )

    @property
    def name(
        self,
    ) -> str:

        return self.NAME

    @property
    def description(
        self,
    ) -> str:

        return self.DESCRIPTION

    def _validate_query(
        self,
        query: str,
    ) -> str:

        query = query.strip()

        if not query:

            raise ValueError(
                "Search query cannot be empty."
            )

        return query

    def _validate_coordinate(
        self,
        latitude: Decimal,
        longitude: Decimal,
    ) -> tuple[Decimal, Decimal]:

        if not (
            Decimal("-90")
            <= latitude
            <= Decimal("90")
        ):
            raise ValueError(
                "Latitude must be between "
                "-90 and 90."
            )

        if not (
            Decimal("-180")
            <= longitude
            <= Decimal("180")
        ):
            raise ValueError(
                "Longitude must be between "
                "-180 and 180."
            )

        return (
            latitude,
            longitude,
        )

    def _request(
        self,
        endpoint: str,
        *,
        params: dict[str, Any],
    ) -> Any:

        url = (
            f"{self.base_url}/{endpoint}"
        )

        logger.info(
            "Requesting Nominatim API "
            f"({endpoint})"
        )

        try:

            response = self.http.get(
                url,
                params=params,
            )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPError as exc:

            logger.exception(
                "Failed requesting "
                "Nominatim API."
            )

            raise RuntimeError(
                "Unable to communicate "
                "with Nominatim."
            ) from exc

    @staticmethod
    def _to_decimal(
        value: str | float,
    ) -> Decimal:

        return Decimal(
            str(value)
        )

    def _parse_place(
        self,
        item: dict[str, Any],
    ) -> PlaceSearchResult:

        address = item.get(
            "address",
            {},
        )

        return PlaceSearchResult(
            name=(
                item.get("name")
                or item.get("display_name", "")
                .split(",")[0]
            ),
            display_name=item.get(
                "display_name",
                "",
            ),
            latitude=self._to_decimal(
                item["lat"],
            ),
            longitude=self._to_decimal(
                item["lon"],
            ),
            city=(
                address.get("city")
                or address.get("town")
                or address.get("village")
            ),
            country=address.get(
                "country",
            ),
            category=item.get(
                "category",
            ),
            place_type=item.get(
                "type",
            ),
        )

    def _parse_forward_geocode(
        self,
        query: str,
        item: dict[str, Any],
    ) -> ForwardGeocodeResult:
        """
        Parse hasil Forward Geocoding.
        """

        return ForwardGeocodeResult(
            query=query,
            latitude=self._to_decimal(
                item["lat"],
            ),
            longitude=self._to_decimal(
                item["lon"],
            ),
            display_name=item.get(
                "display_name",
                "",
            ),
        )

    def _parse_reverse_geocode(
        self,
        item: dict[str, Any],
    ) -> ReverseGeocodeResult:

        address = item.get(
            "address",
            {},
        )

        return ReverseGeocodeResult(
            latitude=self._to_decimal(
                item["lat"],
            ),
            longitude=self._to_decimal(
                item["lon"],
            ),
            display_name=item.get(
                "display_name",
                "",
            ),
            city=(
                address.get("city")
                or address.get("town")
                or address.get("village")
            ),
            country=address.get(
                "country",
            ),
            postcode=address.get(
                "postcode",
            ),
        )

    @staticmethod
    def _ensure_result(
        data: Any,
        message: str,
    ) -> None:

        if not data:

            raise RuntimeError(
                message,
            )
    
    def search_place(
        self,
        query: str,
        *,
        limit: int = 5,
    ) -> list[PlaceSearchResult]:

        query = self._validate_query(
            query,
        )

        if limit < 1:
            raise ValueError(
                "Limit must be greater than zero."
            )

        if limit > 20:
            raise ValueError(
                "Limit cannot be greater than 20."
            )

        logger.info(
            "Searching place "
            f"({query})"
        )

        data = self._request(
            "search",
            params={
                "q": query,
                "format": "jsonv2",
                "addressdetails": 1,
                "limit": limit,
            },
        )

        self._ensure_result(
            data,
            "Place not found.",
        )

        results = [
            self._parse_place(
                item,
            )
            for item in data
        ]

        logger.info(
            f"Found {len(results)} place(s)."
        )

        return results
    
    def forward_geocode(
        self,
        query: str,
    ) -> ForwardGeocodeResult:

        query = self._validate_query(
            query,
        )

        logger.info(
            "Forward geocoding "
            f"({query})"
        )

        data = self._request(
            "search",
            params={
                "q": query,
                "format": "jsonv2",
                "limit": 1,
            },
        )

        self._ensure_result(
            data,
            "Location not found.",
        )

        result = (
            self._parse_forward_geocode(
                query,
                data[0],
            )
        )

        logger.info(
            "Forward geocoding success."
        )

        return result

    def reverse_geocode(
        self,
        latitude: Decimal,
        longitude: Decimal,
    ) -> ReverseGeocodeResult:

        (
            latitude,
            longitude,
        ) = self._validate_coordinate(
            latitude,
            longitude,
        )

        logger.info(
            "Reverse geocoding "
            f"({latitude}, {longitude})"
        )

        data = self._request(
            "reverse",
            params={
                "lat": str(latitude),
                "lon": str(longitude),
                "format": "jsonv2",
                "addressdetails": 1,
            },
        )

        self._ensure_result(
            data,
            "Location not found.",
        )

        result = (
            self._parse_reverse_geocode(
                data,
            )
        )

        logger.info(
            "Reverse geocoding success."
        )

        return result

    def run(
        self,
        **kwargs: Any,
    ) -> (
        list[PlaceSearchResult]
        | ForwardGeocodeResult
        | ReverseGeocodeResult
    ):

        action = (
            kwargs.get(
                "action",
                "",
            )
            .strip()
            .lower()
        )

        logger.info(
            f"PlaceSearchTool started ({action})"
        )

        try:

            if action == self.ACTION_SEARCH:
                
                return self.search_place(
                    query=kwargs["query"],
                    limit=kwargs.get(
                        "limit",
                        5,
                    ),
                )

            if action == self.ACTION_FORWARD_GEOCODE:

                return self.forward_geocode(
                    query=kwargs["query"],
                )

            if action == self.ACTION_REVERSE_GEOCODE:

                return self.reverse_geocode(
                    latitude=Decimal(
                        str(
                            kwargs["latitude"]
                        )
                    ),
                    longitude=Decimal(
                        str(
                            kwargs["longitude"]
                        )
                    ),
                )

            raise ValueError(
                f"Unsupported action: {action}"
            )

        except Exception:

            logger.exception(
                "PlaceSearchTool execution failed."
            )

            raise

        finally:

            logger.info(
                "PlaceSearchTool finished."
            )

    def __del__(
        self,
    ) -> None:

        try:

            self.http.close()

        except Exception:

            pass