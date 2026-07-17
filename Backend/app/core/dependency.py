from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

# Service yang sudah ada sebelumnya
from app.services.auth_service import AuthService
from app.services.calendar_service import CalendarService
from app.services.chat_service import ChatService
from app.services.history_service import HistoryService
from app.services.trip_service import TripService
from app.services.user_service import UserService

# Tambahkan import Service baru di sini
from app.services.saved_place_service import SavedPlaceService
from app.services.tool_log_service import ToolLogService
from app.services.document_service import DocumentService  # Atau RagService sesuaikan dengan struktur Anda


# ==========================================================
# DATABASE SESSION
# ==========================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency untuk Database Session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# USER SERVICE
# ==========================================================

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


# ==========================================================
# AUTH SERVICE
# ==========================================================

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    return AuthService(db)


# ==========================================================
# TRIP SERVICE
# ==========================================================

def get_trip_service(
    db: Session = Depends(get_db),
) -> TripService:
    return TripService(db)


# ==========================================================
# CHAT SERVICE
# ==========================================================

def get_chat_service(
    db: Session = Depends(get_db),
) -> ChatService:
    return ChatService(db)


# ==========================================================
# CALENDAR SERVICE
# ==========================================================

def get_calendar_service(
    db: Session = Depends(get_db),
) -> CalendarService:
    return CalendarService(db)


# ==========================================================
# HISTORY SERVICE
# ==========================================================

def get_history_service(
    db: Session = Depends(get_db),
) -> HistoryService:
    return HistoryService(db)


# ==========================================================
# SAVED PLACE SERVICE (Baru)
# ==========================================================

def get_saved_place_service(
    db: Session = Depends(get_db),
) -> SavedPlaceService:
    """
    Dependency untuk Saved Place Service.
    """
    return SavedPlaceService(db)


# ==========================================================
# TOOL LOG SERVICE (Baru)
# ==========================================================

def get_tool_log_service(
    db: Session = Depends(get_db),
) -> ToolLogService:
    """
    Dependency untuk Tool Log Service.
    """
    return ToolLogService(db)


# ==========================================================
# DOCUMENT SERVICE / RAG (Baru)
# ==========================================================

def get_document_service(
    db: Session = Depends(get_db),
) -> DocumentService:
    """
    Dependency untuk Document Service (RAG Knowledge Base).
    """
    return DocumentService(db)