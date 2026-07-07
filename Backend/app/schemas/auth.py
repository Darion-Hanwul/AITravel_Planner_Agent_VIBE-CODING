from pydantic import BaseModel, EmailStr, Field


# ==========================================================
# REGISTER REQUEST
# ==========================================================

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):

    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
    )

    model_config = ConfigDict(
        extra="forbid",
    )


# ==========================================================
# LOGIN REQUEST
# ==========================================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str

    model_config = ConfigDict(
        extra="forbid",
    )


# ==========================================================
# TOKEN RESPONSE
# ==========================================================

class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


# ==========================================================
# REFRESH TOKEN REQUEST
# ==========================================================

class RefreshTokenRequest(BaseModel):

    refresh_token: str

    model_config = ConfigDict(
        extra="forbid",
    )

# ==========================================================
# CHANGE PASSWORD
# ==========================================================

class ChangePasswordRequest(BaseModel):

    old_password: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=100,
    )

    model_config = ConfigDict(
        extra="forbid",
    )