from __future__ import annotations

from pathlib import Path

from app.ai.models.retrieved_document import RetrievedDocument


class PromptBuilder:
    """
    Builder untuk menyusun prompt yang akan
    dikirim ke LLM.

    Responsibility
    --------------

    - Load prompt template
    - Menyusun context
    - Menyusun history
    - Menyusun final prompt

    Tidak bertanggung jawab terhadap

    - LLM
    - Embedding
    - Retrieval
    - RAG
    """

    PROMPT_DIR = (
        Path(__file__)
        .resolve()
        .parents[1]
        / "prompts"
    )

    # =====================================================
    # PRIVATE
    # =====================================================

    def _load_prompt(
        self,
        filename: str,
    ) -> str:
        """
        Membaca isi file prompt.
        """

        path = self.PROMPT_DIR / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Prompt file '{filename}' not found."
            )

        return path.read_text(
            encoding="utf-8",
        ).strip()

    def _build_context(
        self,
        documents: list[RetrievedDocument],
    ) -> str:
        """
        Mengubah retrieved document menjadi context.
        """

        if not documents:
            return ""

        sections: list[str] = []

        for index, document in enumerate(
            documents,
            start=1,
        ):
            sections.append(
                (
                    f"[Document {index}]\n"
                    f"{document.content}"
                )
            )

        return "\n\n".join(
            sections,
        )

    def _build_history(
        self,
        history: list[str] | None,
    ) -> str:
        """
        Mengubah conversation history
        menjadi string.
        """

        if not history:
            return ""

        return "\n".join(
            history,
        )

    # =====================================================
    # PUBLIC
    # =====================================================

    def build(
        self,
        system_prompt: str,
        task_prompt: str,
        question: str,
        documents: list[RetrievedDocument] | None = None,
        history: list[str] | None = None,
    ) -> str:
        """
        Menyusun prompt lengkap.
        """

        context = self._build_context(
            documents or [],
        )

        conversation = self._build_history(
            history,
        )

        prompt_parts = [
            system_prompt.strip(),
            "",
            task_prompt.strip(),
        ]

        if context:
            prompt_parts.extend(
                [
                    "",
                    "## Context",
                    context,
                ]
            )

        if conversation:
            prompt_parts.extend(
                [
                    "",
                    "## Conversation History",
                    conversation,
                ]
            )

        prompt_parts.extend(
            [
                "",
                "## User Question",
                question.strip(),
            ]
        )

        return "\n".join(
            prompt_parts,
        )

    # =====================================================
    # PROMPT LOADER
    # =====================================================

    def system_prompt(self) -> str:
        return self._load_prompt(
            "system.txt",
        )

    def planner_prompt(self) -> str:
        return self._load_prompt(
            "planner.txt",
        )

    def rag_prompt(self) -> str:
        return self._load_prompt(
            "rag.txt",
        )

    def research_prompt(self) -> str:
        return self._load_prompt(
            "research.txt",
        )

    def budget_prompt(self) -> str:
        return self._load_prompt(
            "budget.txt",
        )

    def schedule_prompt(self) -> str:
        return self._load_prompt(
            "schedule.txt",
        )

    def safety_prompt(self) -> str:
        return self._load_prompt(
            "safety.txt",
        )