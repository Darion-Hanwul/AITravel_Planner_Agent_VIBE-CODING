from __future__ import annotations

from langchain_core.messages import AIMessage

from app.ai.models.ollama import OllamaModel
from app.ai.prompt_builder import PromptBuilder
from app.ai.services.retriever_service import RetrieverService


class RAGService:

    def __init__(
        self,
        *,
        temperature: float | None = None,
    ) -> None:

        self.chat_model = OllamaModel.get_chat_model(
            temperature=temperature,
        )

        self.retriever = RetrieverService()

        self.prompt_builder = PromptBuilder()

    def _extract_response(
        self,
        response: AIMessage,
    ) -> str:
        if isinstance(
            response.content,
            str,
        ):
            return response.content

        return "\n".join(
            str(item)
            for item in response.content
        )

    def _build_prompt(
        self,
        question: str,
        history: list[str] | None,
        top_k: int | None,
    ) -> str:
        documents = self.retriever.hybrid_search(
            query=question,
            limit=top_k,
        )

        return self.prompt_builder.build(
            system_prompt=self.prompt_builder.system_prompt(),
            task_prompt=self.prompt_builder.rag_prompt(),
            question=question,
            documents=documents,
            history=history,
        )

    def ask(
        self,
        question: str,
        history: list[str] | None = None,
        top_k: int | None = None,
    ) -> str:
        prompt = self._build_prompt(
            question=question,
            history=history,
            top_k=top_k,
        )

        response = self.chat_model.invoke(
            prompt,
        )

        return self._extract_response(
            response,
        )

    def close(self) -> None:

        self.retriever.close()