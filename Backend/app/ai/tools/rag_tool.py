from __future__ import annotations

from typing import Any

from app.ai.services.rag_service import RAGService
from app.ai.tools.base_tool import BaseTool
from app.core.logger import logger


class RAGTool(BaseTool):

    NAME = "rag"

    DESCRIPTION = (
        "Answer user questions using Retrieval-Augmented "
        "Generation (RAG) over the travel knowledge base."
    )

    def __init__(
        self,
        *,
        enabled: bool = True,
    ) -> None:
        """
        Initialize RAG Tool.
        """
        super().__init__(
            enabled=enabled,
        )

    @property
    def name(
        self,
    ) -> str:

        return self.NAME

    @property
    def description(
        self,
    ) -> str:

        return self.DESCRIPTION
    
    def _create_service(
        self,
        *,
        temperature: float | None = None,
    ) -> RAGService:

        logger.debug(
            "Creating RAGService instance."
        )

        return RAGService(
            temperature=temperature,
        )
    
    def run(
        self,
        **kwargs: Any,
    ) -> str:

        question = kwargs.get("question")

        if not question:
            raise ValueError(
                "question is required."
            )

        history = kwargs.get(
            "history",
        )

        if history is not None and not isinstance(
            history,
            list,
        ):
            raise ValueError(
                "history must be list[str]."
            )

        top_k = kwargs.get(
            "top_k",
        )

        if top_k is not None and top_k < 1:
            raise ValueError(
                "top_k must be greater than zero."
            )

        temperature = kwargs.get(
            "temperature",
        )

        if (
            temperature is not None
            and not (
                0 <= temperature <= 2
            )
        ):
            raise ValueError(
                "temperature must be between 0 and 2."
            )

        logger.info(
            "RAGTool started."
        )

        logger.debug(
            "Question received."
        ) 

        service = self._create_service(
            temperature=temperature,
        )

        try:

            response = service.ask(
                question=question,
                history=history,
                top_k=top_k,
            )

            logger.info(
                "RAG response generated successfully."
            )

            logger.debug(
                "Response length: %d",
                len(response),
            )

            return response

        except Exception:

            logger.exception(
                "RAGTool execution failed."
            )

            raise

        finally:

            try:

                service.close()

            except Exception:

                logger.exception(
                    "Failed closing RAGService."
                )

            logger.info(
                "RAGTool finished."
            )