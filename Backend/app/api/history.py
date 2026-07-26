from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_history_service
from app.core.exceptions import ChatSessionNotFoundError
from app.schemas.chat import ChatMessageResponse
from app.services.auth_service import AuthService
from app.services.history_service import HistoryService

logger = logging.getLogger("app.api.history")

router = APIRouter(prefix="/history", tags=["Chat History"])

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


@router.get("/{session_id}", response_model=list[ChatMessageResponse])
def get_chat_history(
    session_id: UUID,
    limit: int | None = Query(default=None, description="Batasi jumlah riwayat pesan yang diambil"),
    current_user: Any = Depends(get_current_user_from_token),
    history_service: HistoryService = Depends(get_history_service),
) -> Any:
    logger.info(f"[History API] Mengambil riwayat sesi {session_id} oleh User ID: {current_user.id}")
    try:
        if limit is not None:
            return history_service.get_recent_history(session_id=session_id, limit=limit)
        return history_service.get_history(session_id=session_id)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/{session_id}/count", response_model=dict[str, int])
def count_chat_messages(
    session_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    history_service: HistoryService = Depends(get_history_service),
) -> Any:
    logger.info(f"[History API] Menghitung total pesan sesi {session_id} oleh User ID: {current_user.id}")
    try:
        total_count = history_service.count_messages(session_id=session_id)
        return {"session_id": session_id, "total_messages": total_count}
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{session_id}/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_chat_history(
    session_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    history_service: HistoryService = Depends(get_history_service),
) -> None:
    logger.info(f"[History API] Membersihkan pesan sesi {session_id} oleh User ID: {current_user.id}")
    try:
        history_service.clear_history(session_id=session_id)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))