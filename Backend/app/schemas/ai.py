from uuid import UUID

from pydantic import BaseModel, Field

class AIChatRequest(BaseModel):

    session_id: UUID

    message: str = Field(..., min_length=1)

class AIChatResponse(BaseModel):

    answer: str

    tools_used: list[str] = []

    sources: list[str] = []

    execution_time: float

class TravelPlanRequest(BaseModel):

    destination: str

    start_date: str

    end_date: str

    budget: float

    currency: str

class TravelPlanResponse(BaseModel):

    trip_id: UUID

    summary: str

    estimated_cost: float

    itinerary_generated: bool