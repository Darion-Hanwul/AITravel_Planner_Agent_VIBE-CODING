from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class ChatSessionBase(BaseModel):

    title: str = Field(..., min_length=2, max_length=150)


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )


class ChatSessionResponse(ChatSessionBase):

    id: UUID

    user_id: UUID

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ChatMessageBase(BaseModel):

    role: str = Field(..., pattern="^(user|assistant|system)$")

    message: str = Field(..., min_length=1)


class ChatMessageCreate(ChatMessageBase):

    message: str = Field(..., min_length=1)


class ChatMessageResponse(ChatMessageBase):

    id: UUID

    session_id: UUID

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ChatSessionDetailResponse(ChatSessionResponse):

    messages: list[ChatMessageResponse] = []