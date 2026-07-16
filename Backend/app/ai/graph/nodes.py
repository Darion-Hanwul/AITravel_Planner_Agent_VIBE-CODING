from __future__ import annotations

import logging
from typing import Any

from app.ai.graph.state import AgentState
from app.ai.agents.research_agent import ResearchAgent
from app.ai.agents.budget_agent import BudgetAgent
from app.ai.agents.schedule_agent import ScheduleAgent
from app.ai.agents.safety_agent import SafetyAgent
from app.ai.agents.planner_agent import PlannerAgent

logger = logging.getLogger("app.ai.graph.nodes")


class GraphNodes:
    """
    Kumpulan Node terisolasi untuk eksekusi langkah-langkah di dalam LangGraph.

    Responsibility
    --------------
    - Menerima state saat ini.
    - Menjalankan agen yang sesuai dengan kebutuhan node.
    - Mengembalikan pembaruan state (*state update*).
    """

    def __init__(
        self,
        *,
        research_agent: ResearchAgent,
        budget_agent: BudgetAgent,
        schedule_agent: ScheduleAgent,
        safety_agent: SafetyAgent,
        planner_agent: PlannerAgent,
    ) -> None:
        self.research_agent = research_agent
        self.budget_agent = budget_agent
        self.schedule_agent = schedule_agent
        self.safety_agent = safety_agent
        self.planner_agent = planner_agent

    def research_node(self, state: AgentState) -> dict[str, Any]:
        """
        Node untuk melakukan riset destinasi wisata.
        """
        logger.info("[Node: Research] Memulai riset destinasi.")
        try:
            report = self.research_agent.research_destination(
                destination=state["destination"],
                query=state["raw_query"],
                documents=state.get("retrieved_documents"),
            )
            return {"research_report": report, "current_step": "research_completed"}
        except Exception as exc:
            logger.exception("[Node: Research] Gagal mengeksekusi riset.")
            return {
                "research_report": "Riset tidak dapat diselesaikan.",
                "errors": state.get("errors", []) + [f"Research error: {str(exc)}"],
            }

    def budget_node(self, state: AgentState) -> dict[str, Any]:
        """
        Node untuk melakukan kalkulasi dan optimasi anggaran.
        """
        logger.info("[Node: Budget] Memulai analisis anggaran.")
        try:
            report = self.budget_agent.analyze_budget(
                destination=state["destination"],
                budget_tier=state["budget_tier"],
                duration_days=state["duration_days"],
                query=state["raw_query"],
                documents=state.get("retrieved_documents"),
            )
            return {"budget_report": report, "current_step": "budget_completed"}
        except Exception as exc:
            logger.exception("[Node: Budget] Gagal menganalisis anggaran.")
            return {
                "budget_report": "Kalkulasi anggaran tidak tersedia.",
                "errors": state.get("errors", []) + [f"Budget error: {str(exc)}"],
            }

    def schedule_node(self, state: AgentState) -> dict[str, Any]:
        """
        Node untuk menyusun alokasi waktu dan itinerary harian.
        """
        logger.info("[Node: Schedule] Memulai penyusunan jadwal.")
        try:
            # Mengasumsikan list aktivitas didapatkan dari ekstraksi awal query
            activities = [state["destination"]]
            report = self.schedule_agent.build_schedule(
                destination=state["destination"],
                duration_days=state["duration_days"],
                activities=activities,
                documents=state.get("retrieved_documents"),
            )
            return {"schedule_report": report, "current_step": "schedule_completed"}
        except Exception as exc:
            logger.exception("[Node: Schedule] Gagal menyusun jadwal.")
            return {
                "schedule_report": "Penyusunan jadwal gagal.",
                "errors": state.get("errors", []) + [f"Schedule error: {str(exc)}"],
            }

    def safety_node(self, state: AgentState) -> dict[str, Any]:
        """
        Node untuk mengevaluasi keamanan, regulasi visa, dan hukum lokal.
        """
        logger.info("[Node: Safety] Memulai evaluasi keselamatan.")
        try:
            report = self.safety_agent.evaluate_safety(
                destination=state["destination"],
                user_nationality=state["user_nationality"],
                documents=state.get("retrieved_documents"),
            )
            return {"safety_report": report, "current_step": "safety_completed"}
        except Exception as exc:
            logger.exception("[Node: Safety] Gagal mengevaluasi keamanan.")
            return {
                "safety_report": "Evaluasi keamanan tidak dapat dilakukan.",
                "errors": state.get("errors", []) + [f"Safety error: {str(exc)}"],
            }

    def planner_node(self, state: AgentState) -> dict[str, Any]:
        """
        Node utama (Orchestrator) untuk menyatukan semua laporan parsial.
        """
        logger.info("[Node: Planner] Memulai konsolidasi rencana akhir.")
        try:
            final_itinerary = self.planner_agent.orchestrate_itinerary(
                destination=state["destination"],
                research_report=state["research_report"],
                budget_report=state["budget_report"],
                schedule_report=state["schedule_report"],
                safety_report=state["safety_report"],
                documents=state.get("retrieved_documents"),
            )
            return {"final_itinerary": final_itinerary, "current_step": "planning_completed"}
        except Exception as exc:
            logger.exception("[Node: Planner] Gagal mengonsolidasikan rencana akhir.")
            return {
                "final_itinerary": "Maaf, draf rencana perjalanan Anda gagal dikonsolidasikan.",
                "errors": state.get("errors", []) + [f"Planner error: {str(exc)}"],
            }