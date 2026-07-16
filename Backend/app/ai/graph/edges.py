from __future__ import annotations

import logging
from typing import Literal
from app.ai.graph.state import AgentState

logger = logging.getLogger("app.ai.graph.edges")


def should_continue_planning(state: AgentState) -> Literal["planner", "error_fallback"]:
    """
    Menentukan apakah graf dapat lanjut ke tahap finalisasi (Planner Node).

    Prinsip 14: Keputusan ini murni deterministik berdasarkan ada/tidaknya
    laporan penting dari agen spesialis pendukung di dalam state.
    """
    logger.info("[Edge Routing] Memeriksa kelayakan laporan spesialis.")
    
    required_reports = [
        state.get("research_report"),
        state.get("budget_report"),
        state.get("schedule_report"),
        state.get("safety_report"),
    ]
    
    # Jika salah satu laporan penting kosong sama sekali (bukan karena gracefully failed)
    # maka alihkan ke node penanganan error khusus.
    if any(report is None for report in required_reports):
        logger.warning("[Edge Routing] Laporan agen spesialis tidak lengkap!")
        return "error_fallback"
        
    logger.info("[Edge Routing] Seluruh laporan agen lengkap. Lanjut ke Planner.")
    return "planner"