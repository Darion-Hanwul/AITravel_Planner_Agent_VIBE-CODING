from __future__ import annotations

import logging
from typing import Literal
from app.ai.graph.state import AgentState

logger = logging.getLogger("app.ai.graph.edges")


def should_continue_planning(state: AgentState) -> Literal["planner", "error_fallback"]:

    logger.info("[Edge Routing] Memeriksa kelayakan laporan spesialis.")
    
    required_reports = [
        state.get("research_report"),
        state.get("budget_report"),
        state.get("schedule_report"),
        state.get("safety_report"),
    ]
    
    if any(report is None for report in required_reports):
        logger.warning("[Edge Routing] Laporan agen spesialis tidak lengkap!")
        return "error_fallback"
        
    logger.info("[Edge Routing] Seluruh laporan agen lengkap. Lanjut ke Planner.")
    return "planner"