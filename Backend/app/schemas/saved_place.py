from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base
# ==========================================================

class SavedPlaceBase(BaseModel):

    name: str = Field(..., min_length=2, max_length=200)

    country: str = Field(..., min_length=2, max_length=100)

    city: str = Field(..., min_length=2, max_length=100)

    latitude: Decimal

    longitude: Decimal

    category: str

    notes: str | None = None


# ==========================================================
# Create
# ==========================================================

class SavedPlaceCreate(SavedPlaceBase):
    pass


# ==========================================================
# Update
# ==========================================================

class SavedPlaceUpdate(BaseModel):

    name: str | None = None

    country: str | None = None

    city: str | None = None

    latitude: Decimal | None = None

    longitude: Decimal | None = None

    category: str | None = None

    notes: str | None = None


# ==========================================================
# Response
# ==========================================================

class SavedPlaceResponse(SavedPlaceBase):

    id: UUID

    user_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )