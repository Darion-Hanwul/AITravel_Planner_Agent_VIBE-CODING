from __future__ import annotations

import logging
from typing import Any

from langgraph.graph import StateGraph, START, END

from app.ai.graph.state import AgentState
from app.ai.graph.nodes import GraphNodes
from app.ai.graph.edges import should_continue_planning

logger = logging.getLogger("app.ai.graph.workflow")


class TravelPlannerWorkflow:
    """
    TravelPlannerWorkflow bertanggung jawab merakit State, Nodes, dan Edges
    menjadi grafik eksekusi (StateGraph) yang siap dikompilasi (Prinsip 1, 2).

    Responsibility
    --------------
    - Mendefinisikan struktur aliran data antar-agen.
    - Menentukan eksekusi paralel untuk agen spesialis guna efisiensi performa (Prinsip 24).
    - Menyediakan antarmuka kompilasi graf untuk digunakan oleh API/Service layer.
    """

    def __init__(self, nodes: GraphNodes) -> None:
        """
        Inisialisasi workflow dengan instance GraphNodes yang membawa dependensi agen.
        
        Args:
            nodes: Instance GraphNodes yang berisi agen-agen yang siap dieksekusi.
        """
        self.nodes = nodes
        self._graph_builder = StateGraph(AgentState)
        self._register_nodes_and_edges()

    def _register_nodes_and_edges(self) -> None:
        """
        Mendaftarkan seluruh node dan mendesain topologi graf aliran kerja.
        """
        logger.info("Memulai konfigurasi topologi LangGraph.")

        # 1. Daftarkan semua Node ke dalam Graph Builder
        self._graph_builder.add_node("research", self.nodes.research_node)
        self._graph_builder.add_node("budget", self.nodes.budget_node)
        self._graph_builder.add_node("schedule", self.nodes.schedule_node)
        self._graph_builder.add_node("safety", self.nodes.safety_node)
        self._graph_builder.add_node("planner", self.nodes.planner_node)

        # 2. Atur Aliran Paralel dari START (Prinsip 21 & 24)
        # Keempat agen spesialis akan mulai bekerja secara bersamaan (Asinkron/Paralel)
        self._graph_builder.add_edge(START, "research")
        self._graph_builder.add_edge(START, "budget")
        self._graph_builder.add_edge(START, "schedule")
        self._graph_builder.add_edge(START, "safety")

        # 3. Definisikan Aliran Penggabungan (Join/Merge)
        # Setelah semua agen spesialis selesai, arahkan ke Planner secara kondisional (Prinsip 14)
        self._graph_builder.add_conditional_edges(
            "research",
            should_continue_planning,
            {
                "planner": "planner",
                "error_fallback": END
            }
        )
        self._graph_builder.add_conditional_edges(
            "budget",
            should_continue_planning,
            {
                "planner": "planner",
                "error_fallback": END
            }
        )
        self._graph_builder.add_conditional_edges(
            "schedule",
            should_continue_planning,
            {
                "planner": "planner",
                "error_fallback": END
            }
        )
        self._graph_builder.add_conditional_edges(
            "safety",
            should_continue_planning,
            {
                "planner": "planner",
                "error_fallback": END
            }
        )

        # 4. Aliran Akhir dari Planner ke END
        self._graph_builder.add_edge("planner", END)

        logger.info("Topologi LangGraph berhasil dikonfigurasi.")

    def compile(self) -> Any:
        """
        Mengompilasi graf menjadi executable runnable yang siap dieksekusi.

        Returns:
            CompiledGraph: Instance graf terkompilasi dari LangGraph.
        """
        try:
            logger.info("Mengompilasi Workflow Graf.")
            return self._graph_builder.compile()
        except Exception as exc:
            logger.exception("Gagal mengompilasi LangGraph.")
            raise RuntimeError("Gagal mengompilasi graf alur agen.") from exc