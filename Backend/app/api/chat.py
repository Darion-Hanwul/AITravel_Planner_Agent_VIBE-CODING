from __future__ import annotations

import logging
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.dependency import get_auth_service, get_chat_service
from app.core.exceptions import ChatSessionNotFoundError
from app.schemas.chat import (
    ChatMessageResponse,
    ChatSessionCreate,
    ChatSessionDetailResponse,
    ChatSessionResponse,
    ChatSessionUpdate,
)
from app.services.auth_service import AuthService
from app.services.chat_service import ChatService

logger = logging.getLogger("app.api.chat")

router = APIRouter(prefix="/chats", tags=["Chat"])

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


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    data: ChatSessionCreate,
    current_user: Any = Depends(get_current_user_from_token),
    chat_service: ChatService = Depends(get_chat_service),
) -> Any:
    logger.info(f"[Chat API] Membuat sesi baru untuk User ID: {current_user.id}")
    return chat_service.create_session(user_id=current_user.id, data=data)


@router.get("/sessions", response_model=list[ChatSessionResponse])
def get_user_sessions(
    current_user: Any = Depends(get_current_user_from_token),
    chat_service: ChatService = Depends(get_chat_service),
) -> Any:
    logger.info(f"[Chat API] Mengambil semua sesi chat milik User ID: {current_user.id}")
    return chat_service.get_user_sessions(user_id=current_user.id)


@router.get("/sessions/{session_id}", response_model=ChatSessionDetailResponse)
def get_session_detail(
    session_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    chat_service: ChatService = Depends(get_chat_service),
) -> Any:
    logger.info(f"[Chat API] Mengambil detail sesi {session_id} untuk User ID: {current_user.id}")
    try:
        session = chat_service.get_session(session_id=session_id)
        messages = chat_service.get_messages(session_id=session_id)
        
        return ChatSessionDetailResponse(
            id=session.id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at,
            messages=messages
        )
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/sessions/{session_id}", response_model=ChatSessionResponse)
def rename_session(
    session_id: UUID,
    data: ChatSessionUpdate,
    current_user: Any = Depends(get_current_user_from_token),
    chat_service: ChatService = Depends(get_chat_service),
) -> Any:
    logger.info(f"[Chat API] Mengubah nama sesi {session_id} oleh User ID: {current_user.id}")
    if data.title is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Field 'title' wajib dikirimkan untuk mengubah nama sesi."
        )
    try:
        return chat_service.rename_session(session_id=session_id, title=data.title)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: UUID,
    current_user: Any = Depends(get_current_user_from_token),
    chat_service: ChatService = Depends(get_chat_service),
) -> None:
    logger.info(f"[Chat API] Menghapus sesi {session_id} oleh User ID: {current_user.id}")
    try:
        chat_service.delete_session(session_id=session_id)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


# KEMBALIKAN KE JALUR RESMI: Validasi token JWT diaktifkan kembali
@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    session_id: UUID,
    message_text: str,  
    current_user: Any = Depends(get_current_user_from_token), # Resmi & Aman
    chat_service: ChatService = Depends(get_chat_service),
) -> Any:
    logger.info(f"[Chat API] Mengirim pesan ke sesi {session_id} oleh User ID: {current_user.id}")
    try:
        return chat_service.send_message(session_id=session_id, message=message_text)
    except ChatSessionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))