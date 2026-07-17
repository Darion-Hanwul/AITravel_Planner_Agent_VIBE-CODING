from __future__ import annotations

import logging
from datetime import date
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_calendar_service
from app.core.exceptions import ResourceNotFoundError, ValidationError
from app.schemas.calendar import (
    CalendarEventCreate,
    CalendarEventResponse,
    CalendarEventUpdate,
)
from app.services.auth_service import AuthService
from app.services.calendar_service import CalendarService

logger = logging.getLogger("app.api.calendar")

router = APIRouter(prefix="/calendar", tags=["Calendar Events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> Any:
    """
    Mengekstrak dan memverifikasi pengguna aktif dari token Bearer.
    """
    try:
        return auth_service.verify_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau kedaluwarsa.",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/events", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    data: CalendarEventCreate,
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> Any:
    """
    Membuat agenda kegiatan baru pada kalender perjalanan.
    """
    logger.info(f"[Calendar API] Membuat event baru untuk User ID: {current_user.id}")
    try:
        return calendar_service.create_event(data=data)
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/events/reminders", response_model=list[CalendarEventResponse])
def get_reminder_events(
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> Any:
    """
    Mengambil semua daftar agenda perjalanan yang memiliki pengingat aktif (reminder=True).
    """
    logger.info(f"[Calendar API] Mengambil semua reminder event untuk User ID: {current_user.id}")
    return calendar_service.get_reminder_events()


@router.get("/events/filter", response_model=list[CalendarEventResponse])
def get_events_by_date_filter(
    target_date: date | None = Query(default=None, alias="date", description="Filter event pada tanggal tertentu"),
    start_date: date | None = Query(default=None, description="Awal rentang tanggal pencarian"),
    end_date: date | None = Query(default=None, description="Akhir rentang tanggal pencarian"),
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> Any:
    """
    Mengambil daftar agenda perjalanan dengan filter fleksibel (berdasarkan tanggal tunggal atau jangkauan rentang waktu).
    """
    logger.info(f"[Calendar API] Melakukan filter agenda untuk User ID: {current_user.id}")
    
    try:
        if start_date is not None and end_date is not None:
            return calendar_service.get_events_between(start_date=start_date, end_date=end_date)
        elif target_date is not None:
            return calendar_service.get_events_by_date(event_date=target_date)
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tentukan parameter kueri 'date' atau kombinasikan 'start_date' & 'end_date'."
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/events/{event_id}", response_model=CalendarEventResponse)
def get_event(
    event_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> Any:
    """
    Mengambil informasi lengkap satu agenda kalender berdasarkan ID.
    """
    logger.info(f"[Calendar API] Mengambil event {event_id} oleh User ID: {current_user.id}")
    try:
        return calendar_service.get_event(event_id=event_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/events/{event_id}", response_model=CalendarEventResponse)
def update_event(
    event_id: UUID,
    data: CalendarEventUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> Any:
    """
    Mengubah rincian informasi, waktu pelaksanaan, atau status pengingat agenda kalender.
    """
    logger.info(f"[Calendar API] Memperbarui event {event_id} oleh User ID: {current_user.id}")
    try:
        return calendar_service.update_event(event_id=event_id, data=data)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    calendar_service: CalendarService = Depends(get_calendar_service),
) -> None:
    """
    Menghapus agenda dari kalender perjalanan secara permanen.
    """
    logger.info(f"[Calendar API] Menghapus event {event_id} oleh User ID: {current_user.id}")
    try:
        calendar_service.delete_event(event_id=event_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))