from __future__ import annotations

from typing import TypedDict, Any
from app.ai.models.retrieved_document import RetrievedDocument


class AgentState(TypedDict):
    """
    Representasi state yang mengalir di setiap node dalam LangGraph.

    Responsibility
    --------------
    - Menyimpan data input awal dari pengguna.
    - Menyimpan dokumen hasil retrieval RAG (Prinsip 17).
    - Menyimpan laporan parsial dari masing-masing agen (Research, Budget, Schedule, Safety).
    - Menyimpan respons final yang akan dikirim kembali ke pengguna.
    - Menyimpan catatan kesalahan jika terjadi kendala di salah satu langkah (Prinsip 10).
    """
    
    destination: str
    travel_dates: str
    duration_days: int
    budget_tier: str  
    user_nationality: str
    raw_query: str

    history: list[str]
    
    retrieved_documents: list[RetrievedDocument]
    
    research_report: str
    budget_report: str
    schedule_report: str
    safety_report: str
    
    final_itinerary: str
    
    errors: list[str]
    current_step: str