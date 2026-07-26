from typing import Optional
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.message import ChatMessage
from app.models.session import ChatSession
from app.repositories.base_repository import BaseRepository


class ChatSessionRepository(
    BaseRepository[ChatSession]
):

    def __init__(self) -> None:
        super().__init__(ChatSession)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[ChatSession]:

        stmt = (
            select(ChatSession)
            .where(
                ChatSession.user_id == user_id
            )
            .order_by(
                ChatSession.created_at.desc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def get_latest_session(
        self,
        db: Session,
        user_id: UUID,
    ) -> Optional[ChatSession]:

        stmt = (
            select(ChatSession)
            .where(
                ChatSession.user_id == user_id
            )
            .order_by(
                ChatSession.created_at.desc()
            )
            .limit(1)
        )

        return db.scalar(stmt)

class ChatMessageRepository(
    BaseRepository[ChatMessage]
):

    def __init__(self) -> None:
        super().__init__(ChatMessage)

    def get_by_session(
        self,
        db: Session,
        session_id: UUID,
    ) -> list[ChatMessage]:

        stmt = (
            select(ChatMessage)
            .where(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def delete_session_messages(
        self,
        db: Session,
        session_id: UUID,
    ) -> None:

        stmt = (
            delete(ChatMessage)
            .where(
                ChatMessage.session_id == session_id
            )
        )

        db.execute(stmt)

    def get_detail(
        self,
        db: Session,
        session_id: UUID,
    ) -> ChatSession | None:
        stmt = (
            select(ChatSession)
            .options(
                joinedload(ChatSession.messages)
            )
        )

    def create_message(
        self,
        db: Session,
        message: ChatMessage,
    ) -> ChatMessage:

        db.add(message)

        return message