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
    ChatSessionCreate,
    ChatSessionResponse,
)

from app.services.base_service import BaseService

class ChatService(BaseService):
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

    #PRIVATE

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
    
    def _generate_title(
        self,
        message: str,
    ) -> str:
        message = message.strip()

        if len(message) <= 150:
            return message

        return message[:150] + "..."
    
    def _create_session(
        self,
        user_id: UUID,
        title: str,
    ) -> ChatSession:

        session = ChatSession(
            user_id=user_id,
            title=title,
        )

        self.chat_session_repository.create(
            self.db,
            session,
        )

        return session
    
    def _create_message(
        self,
        session_id: UUID,
        role: str,
        message: str,
    ) -> ChatMessage:

        chat_message = ChatMessage(
            session_id=session_id,
            role=role,
            message=message,
        )

        self.chat_message_repository.create(
            self.db,
            chat_message,
        )

        return chat_message

    def _to_session_response(
        self,
        session: ChatSession,
    ) -> ChatSessionResponse:

        return ChatSessionResponse.model_validate(
            session,
        )
    
    def _to_message_response(
        self,
        message: ChatMessage,
    ) -> ChatMessageResponse:

        return ChatMessageResponse.model_validate(
            message,
        )
    
    def _save_user_message(
        self,
        session_id: UUID,
        message: str,
    ) -> ChatMessage:

        return self._create_message(
            session_id=session_id,
            role="user",
            message=message,
        )
    
    def _save_ai_message(
        self,
        session_id: UUID,
        message: str,
    ) -> ChatMessage:

        return self._create_message(
            session_id=session_id,
            role="assistant",
            message=message,
        )

    def create_session(
        self,
        user_id: UUID,
        data: ChatSessionCreate,
    ) -> ChatSessionResponse:

        try:

            session = self._create_session(
                user_id=user_id,
                title=data.title,
            )

            self.commit()

            self.refresh(
                session,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_session_response(
            session,
        )
    
    def get_session(
        self,
        session_id: UUID,
    ) -> ChatSessionResponse:

        session = self._get_session(
            session_id,
        )

        return self._to_session_response(
            session,
        )
    
    def get_user_sessions(
        self,
        user_id: UUID,
    ) -> list[ChatSessionResponse]:

        sessions = (
            self.chat_session_repository.get_by_user(
                self.db,
                user_id,
            )
        )

        return [
            self._to_session_response(
                session,
            )
            for session in sessions
        ]
    
    def rename_session(
        self,
        session_id: UUID,
        title: str,
    ) -> ChatSessionResponse:
        session = self._get_session(
            session_id,
        )

        session.title = title

        try:

            self.chat_session_repository.update(
                self.db,
                session,
            )

            self.commit()

            self.refresh(
                session,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_session_response(
            session,
        )
    
    def get_messages(
        self,
        session_id: UUID,
    ) -> list[ChatMessageResponse]:

        self._get_session(
            session_id,
        )

        messages = (
            self.chat_message_repository.get_by_session(
                self.db,
                session_id,
            )
        )

        return [
            self._to_message_response(
                message,
            )
            for message in messages
        ]
    
    def send_message(
        self,
        session_id: UUID,
        message: str,
    ) -> ChatMessageResponse:

        session = self._get_session(
            session_id,
        )

        user_message = self._save_user_message(
            session.id,
            message,
        )

        try:

            self.chat_message_repository.create(
                self.db,
                user_message,
            )

            self.commit()

            self.refresh(
                user_message,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_message_response(
            user_message,
        )
        
    def delete_session(
        self,
        session_id: UUID,
    ) -> None:

        session = self._get_session(
            session_id,
        )

        try:

            self.chat_session_repository.delete(
                self.db,
                session,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise