from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ==========================================================
# Base
# ==========================================================

class DocumentBase(BaseModel):

    title: str = Field(..., min_length=2, max_length=255)

    file_name: str = Field(..., min_length=2)

    source: str = Field(..., min_length=2)


# ==========================================================
# Upload
# ==========================================================

class DocumentUpload(BaseModel):

    title: str = Field(..., min_length=2, max_length=255)


# ==========================================================
# Response
# ==========================================================

class DocumentResponse(DocumentBase):

    id: UUID

    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )