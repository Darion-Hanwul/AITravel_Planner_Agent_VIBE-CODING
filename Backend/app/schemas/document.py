from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class DocumentBase(BaseModel):

    title: str = Field(..., min_length=2, max_length=255)

    file_name: str = Field(..., min_length=2)

    source: str = Field(..., min_length=2)

class DocumentUpload(BaseModel):

    title: str = Field(..., min_length=2, max_length=255)

class DocumentResponse(DocumentBase):

    id: UUID

    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )