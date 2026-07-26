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
from app.services.document_service import DocumentService  

def get_db() -> Generator[Session, None, None]:
    """
    Dependency untuk Database Session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    return AuthService(db)

def get_trip_service(
    db: Session = Depends(get_db),
) -> TripService:
    return TripService(db)

def get_chat_service(
    db: Session = Depends(get_db),
) -> ChatService:
    return ChatService(db)

def get_calendar_service(
    db: Session = Depends(get_db),
) -> CalendarService:
    return CalendarService(db)

def get_history_service(
    db: Session = Depends(get_db),
) -> HistoryService:
    return HistoryService(db)

def get_saved_place_service(
    db: Session = Depends(get_db),
) -> SavedPlaceService:
    return SavedPlaceService(db)

def get_tool_log_service(
    db: Session = Depends(get_db),
) -> ToolLogService:
    return ToolLogService(db)

def get_document_service(
    db: Session = Depends(get_db),
) -> DocumentService:
    return DocumentService(db)