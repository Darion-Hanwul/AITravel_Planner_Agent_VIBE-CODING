from uuid import UUID

from pydantic import BaseModel, Field


# ==========================================================
# Chat Request
# ==========================================================

class AIChatRequest(BaseModel):

    session_id: UUID

    message: str = Field(..., min_length=1)


# ==========================================================
# AI Response
# ==========================================================

class AIChatResponse(BaseModel):

    answer: str

    tools_used: list[str] = []

    sources: list[str] = []

    execution_time: float


# ==========================================================
# Planner Request
# ==========================================================

class TravelPlanRequest(BaseModel):

    destination: str

    start_date: str

    end_date: str

    budget: float

    currency: str


# ==========================================================
# Planner Response
# ==========================================================

class TravelPlanResponse(BaseModel):

    trip_id: UUID

    summary: str

    estimated_cost: float

    itinerary_generated: bool