from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class ToolExecutionRequest(BaseModel):

    tool_name: str = Field(..., min_length=2)

    input_data: dict

class ToolExecutionResponse(BaseModel):

    tool_name: str

    success: bool

    output_data: dict

class ToolLogResponse(BaseModel):

    id: UUID

    trip_id: UUID

    tool_name: str

    input: str

    output: str

    status: str

    execution_time_ms: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )