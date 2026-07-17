from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_saved_place_service
from app.core.exceptions import ResourceNotFoundError
from app.schemas.saved_place import SavedPlaceCreate, SavedPlaceResponse, SavedPlaceUpdate
from app.services.auth_service import AuthService
from app.services.saved_place_service import SavedPlaceService

logger = logging.getLogger("app.api.saved_place")
router = APIRouter(prefix="/saved-places", tags=["Saved Places"])
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
            detail="Token tidak valid atau kedaluwarsa.",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("", response_model=SavedPlaceResponse, status_code=status.HTTP_201_CREATED)
def create_saved_place(
    data: SavedPlaceCreate,
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> Any:
    logger.info(f"[SavedPlace API] Membuat saved place baru untuk User ID: {current_user.id}")
    return saved_place_service.create_place(user_id=current_user.id, data=data)

@router.get("", response_model=list[SavedPlaceResponse])
def get_user_saved_places(
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> Any:
    logger.info(f"[SavedPlace API] Mengambil semua tempat simpanan User ID: {current_user.id}")
    return saved_place_service.get_user_places(user_id=current_user.id)

@router.get("/search", response_model=list[SavedPlaceResponse])
def search_saved_places(
    keyword: str = Query(..., description="Kata kunci nama tempat"),
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> Any:
    logger.info(f"[SavedPlace API] Pencarian tempat dengan keyword '{keyword}' oleh User ID: {current_user.id}")
    return saved_place_service.search_place(user_id=current_user.id, keyword=keyword)

@router.get("/{place_id}", response_model=SavedPlaceResponse)
def get_saved_place_detail(
    place_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> Any:
    logger.info(f"[SavedPlace API] Detail tempat {place_id} oleh User ID: {current_user.id}")
    try:
        return saved_place_service.get_place(place_id=place_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.put("/{place_id}", response_model=SavedPlaceResponse)
def update_saved_place(
    place_id: UUID,
    data: SavedPlaceUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> Any:
    logger.info(f"[SavedPlace API] Update tempat {place_id} oleh User ID: {current_user.id}")
    try:
        return saved_place_service.update_place(place_id=place_id, data=data)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved_place(
    place_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    saved_place_service: SavedPlaceService = Depends(get_saved_place_service),
) -> None:
    logger.info(f"[SavedPlace API] Menghapus tempat {place_id} oleh User ID: {current_user.id}")
    try:
        saved_place_service.delete_place(place_id=place_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))