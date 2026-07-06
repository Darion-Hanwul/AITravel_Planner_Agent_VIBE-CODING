from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.session import ChatSession
from app.models.message import ChatMessage

from app.repositories.base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):

    def __init__(self):
        super().__init__(ChatSession)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[ChatSession]:

        return (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
            .all()
        )

    def get_latest_session(
        self,
        db: Session,
        user_id: UUID,
    ) -> Optional[ChatSession]:

        return (
            db.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
            .first()
        )


class ChatMessageRepository(BaseRepository[ChatMessage]):

    def __init__(self):
        super().__init__(ChatMessage)

    def get_by_session(
        self,
        db: Session,
        session_id: UUID,
    ) -> list[ChatMessage]:

        return (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

    def delete_session_messages(
        self,
        db: Session,
        session_id: UUID,
    ) -> None:

        (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .delete()
        )

        db.commit()