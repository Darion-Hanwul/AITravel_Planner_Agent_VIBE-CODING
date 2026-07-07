from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ==========================================================
# Base Schema
# ==========================================================

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr


# ==========================================================
# Create
# ==========================================================

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    model_config = ConfigDict(
        extra="forbid",
    )

# ==========================================================
# Update
# ==========================================================

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3, max_length=100)
    avatar_url: str | None = None
    model_config = ConfigDict(
        extra="forbid",
    )

# ==========================================================
# Response
# ==========================================================

class UserResponse(UserBase):
    id: UUID
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

# ==========================================================
# USER PREFERENCE
# ==========================================================


class UserPreferenceBase(BaseModel):
    preferred_currency: str
    budget_min: float
    budget_max: float

    favorite_country: str | None = None
    favorite_food: str | None = None

    hotel_star: int | None = None

    travel_style: str | None = None

    transportation_preference: str | None = None


class UserPreferenceUpdate(BaseModel):
    preferred_currency: str | None = None

    budget_min: float | None = None

    budget_max: float | None = None

    favorite_country: str | None = None

    favorite_food: str | None = None

    hotel_star: int | None = None

    travel_style: str | None = None

    transportation_preference: str | None = None

    model_config = ConfigDict(
        extra="forbid",
    )

class UserPreferenceResponse(UserPreferenceBase):

    id: UUID

    user_id: UUID

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class UserProfileResponse(UserResponse):

    preferences: UserPreferenceResponse | None = None