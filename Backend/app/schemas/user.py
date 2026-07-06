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


# ==========================================================
# Update
# ==========================================================

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=3, max_length=100)
    avatar_url: str | None = None


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