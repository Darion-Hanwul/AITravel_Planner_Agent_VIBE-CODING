from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

class SavedPlaceBase(BaseModel):

    name: str = Field(..., min_length=2, max_length=200)

    country: str = Field(..., min_length=2, max_length=100)

    city: str = Field(..., min_length=2, max_length=100)

    latitude: Decimal

    longitude: Decimal

    category: str

    notes: str | None = None

class SavedPlaceCreate(SavedPlaceBase):
    pass

class SavedPlaceUpdate(BaseModel):

    name: str | None = None

    country: str | None = None

    city: str | None = None

    latitude: Decimal | None = None

    longitude: Decimal | None = None

    category: str | None = None

    notes: str | None = None

class SavedPlaceResponse(SavedPlaceBase):

    id: UUID

    user_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )

class PlaceSearchResult(BaseModel):
    """
    Hasil pencarian lokasi dari
    Nominatim API.
    """

    name: str

    display_name: str

    latitude: Decimal

    longitude: Decimal

    city: str | None = None

    country: str | None = None

    category: str | None = None

    place_type: str | None = None

class ForwardGeocodeResult(BaseModel):
    """
    Hasil geocoding dari nama lokasi
    menjadi koordinat.
    """

    query: str

    latitude: Decimal

    longitude: Decimal

    display_name: str

class ReverseGeocodeResult(BaseModel):
    """
    Hasil reverse geocoding dari
    koordinat menjadi alamat.
    """

    latitude: Decimal

    longitude: Decimal

    display_name: str

    city: str | None = None

    country: str | None = None

    postcode: str | None = None