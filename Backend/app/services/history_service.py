from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ChatSessionNotFoundError,
)

from app.models.message import ChatMessage
from app.models.session import ChatSession

from app.repositories.chat_repository import (
    ChatMessageRepository,
    ChatSessionRepository,
)

from app.schemas.chat import (
    ChatMessageResponse,
)

from app.services.base_service import BaseService


class HistoryService(BaseService):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.chat_session_repository = (
            ChatSessionRepository()
        )

        self.chat_message_repository = (
            ChatMessageRepository()
        )

    def _get_session(
        self,
        session_id: UUID,
    ) -> ChatSession:
        session = (
            self.chat_session_repository.get_by_id(
                self.db,
                session_id,
            )
        )

        if session is None:
            raise ChatSessionNotFoundError(
                "Chat session not found.",
            )

        return session

    def _get_messages(
        self,
        session_id: UUID,
    ) -> list[ChatMessage]:

        self._get_session(session_id)

        return (
            self.chat_message_repository.get_by_session(
                self.db,
                session_id,
            )
        )

    def _limit_history(
        self,
        messages: list[ChatMessage],
        limit: int,
    ) -> list[ChatMessage]:
        if limit <= 0:
            return messages

        return messages[-limit:]

    def _build_history(
        self,
        messages: list[ChatMessage],
    ) -> list[dict[str, str]]:
        return [
            {
                "role": message.role,
                "content": message.message,
            }
            for message in messages
        ]

    def _to_message_response(
        self,
        message: ChatMessage,
    ) -> ChatMessageResponse:
        return ChatMessageResponse.model_validate(
            message,
        )

    def get_history(
        self,
        session_id: UUID,
    ) -> list[ChatMessageResponse]:
        messages = self._get_messages(
            session_id,
        )

        return [
            self._to_message_response(
                message,
            )
            for message in messages
        ]

    def get_recent_history(
        self,
        session_id: UUID,
        limit: int = 10,
    ) -> list[ChatMessageResponse]:

        messages = self._get_messages(
            session_id,
        )

        messages = self._limit_history(
            messages,
            limit,
        )

        return [
            self._to_message_response(
                message,
            )
            for message in messages
        ]

    def build_context(
        self,
        session_id: UUID,
        limit: int = 10,
    ) -> list[dict[str, str]]:
        messages = self._get_messages(
            session_id,
        )

        messages = self._limit_history(
            messages,
            limit,
        )

        return self._build_history(
            messages,
        )

    def count_messages(
        self,
        session_id: UUID,
    ) -> int:
        messages = self._get_messages(
            session_id,
        )

        return len(messages)

    def clear_history(
        self,
        session_id: UUID,
    ) -> None:
        self._get_session(
            session_id,
        )

        try:

            self.chat_message_repository.delete_session_messages(
                self.db,
                session_id,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise