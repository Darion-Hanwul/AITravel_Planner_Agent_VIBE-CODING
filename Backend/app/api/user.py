from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_user_service
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.schemas.user import (
    UserPreferenceResponse,
    UserPreferenceUpdate,
    UserProfileResponse,
    UserResponse,
    UserUpdate,
)
from app.services.auth_service import AuthService
from app.services.user_service import UserService

logger = logging.getLogger("app.api.user")
router = APIRouter(prefix="/users", tags=["User Profile"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")

def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    try:
        return auth_service.verify_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesi berakhir, silakan masuk kembali.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user: Any = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    logger.info(f"[User API] Mengambil profil lengkap User ID: {current_user.id}")
    try:
        return user_service.get_profile(user_id=current_user.id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.put("/me", response_model=UserResponse)
def update_my_profile(
    data: UserUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    logger.info(f"[User API] Memperbarui informasi profil User ID: {current_user.id}")
    try:
        return user_service.update_profile(user_id=current_user.id, data=data)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch("/me/avatar", response_model=UserResponse)
def update_my_avatar(
    avatar_url: str,
    current_user: Any = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    logger.info(f"[User API] Mengubah tautan avatar User ID: {current_user.id}")
    try:
        return user_service.update_avatar(user_id=current_user.id, avatar_url=avatar_url)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get("/me/preferences", response_model=UserPreferenceResponse)
def get_my_preferences(
    current_user: Any = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    logger.info(f"[User API] Mengambil preferensi User ID: {current_user.id}")
    try:
        return user_service.get_preferences(user_id=current_user.id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.put("/me/preferences", response_model=UserPreferenceResponse)
def update_my_preferences(
    data: UserPreferenceUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    user_service: UserService = Depends(get_user_service),
) -> Any:
    logger.info(f"[User API] Memperbarui kriteria preferensi User ID: {current_user.id}")
    try:
        return user_service.update_preferences(user_id=current_user.id, data=data)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))