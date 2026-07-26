from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.constants import TripStatus
from app.core.dependency import get_auth_service, get_trip_service
from app.core.exceptions import TripNotFoundError, TripValidationError
from app.schemas.trip import (
    TripCreate,
    TripDetailResponse,
    TripResponse,
    TripUpdate,
)
from app.services.auth_service import AuthService
from app.services.trip_service import TripService

logger = logging.getLogger("app.api.trip")

router = APIRouter(prefix="/trips", tags=["Trips"])

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


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    data: TripCreate,
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> Any:
    logger.info(f"[Trip API] User ID: {current_user.id} merencanakan trip baru ke {data.destination}")
    try:
        return trip_service.create_trip(user_id=current_user.id, data=data)
    except TripValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("", response_model=list[TripResponse])
def get_user_trips(
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> Any:
    logger.info(f"[Trip API] Mengambil semua daftar trip milik User ID: {current_user.id}")
    return trip_service.get_user_trips(user_id=current_user.id)


@router.get("/{trip_id}", response_model=TripDetailResponse)
def get_trip_detail(
    trip_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> Any:
    logger.info(f"[Trip API] Mengambil detail Trip ID: {trip_id} oleh User ID: {current_user.id}")
    try:
        # Lakukan validasi hak kepemilikan manual tingkat API jika service layer mengembalikan objek murni
        trip_response = trip_service.get_trip(trip_id=trip_id)
        if trip_response.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Anda tidak memiliki hak akses terhadap rencana perjalanan ini."
            )
            
        return trip_service.get_trip_detail(trip_id=trip_id)
    except TripNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: UUID,
    data: TripUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> Any:
    logger.info(f"[Trip API] Memperbarui Trip ID: {trip_id} oleh User ID: {current_user.id}")
    try:
        trip_response = trip_service.get_trip(trip_id=trip_id)
        if trip_response.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Anda tidak memiliki hak akses mengubah rencana perjalanan ini."
            )
            
        return trip_service.update_trip(trip_id=trip_id, data=data)
    except TripNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TripValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> None:
    logger.info(f"[Trip API] Menghapus Trip ID: {trip_id} oleh User ID: {current_user.id}")
    try:
        trip_response = trip_service.get_trip(trip_id=trip_id)
        if trip_response.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Anda tidak memiliki hak akses menghapus rencana perjalanan ini."
            )
            
        trip_service.delete_trip(trip_id=trip_id)
    except TripNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{trip_id}/status", response_model=TripResponse)
def change_trip_status(
    trip_id: UUID,
    status_enum: TripStatus,
    current_user: Any = Depends(get_current_user_from_token),
    trip_service: TripService = Depends(get_trip_service),
) -> Any:
    logger.info(f"[Trip API] Mengubah status Trip ID: {trip_id} menjadi {status_enum} oleh User ID: {current_user.id}")
    try:
        trip_response = trip_service.get_trip(trip_id=trip_id)
        if trip_response.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Anda tidak memiliki hak akses memodifikasi perjalanan ini."
            )
            
        return trip_service.change_status(trip_id=trip_id, status=status_enum)
    except TripNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))