from __future__ import annotations

from typing import Any

from app.ai.services.rag_service import RAGService
from app.ai.tools.base_tool import BaseTool
from app.core.logger import logger


class RAGTool(BaseTool):
    """
    Retrieval-Augmented Generation (RAG) Tool.

    Responsibility
    --------------

    - Menjadi adapter antara AI Agent dan RAGService.
    - Meneruskan permintaan retrieval ke RAGService.
    - Mengelola lifecycle RAGService.
    - Logging proses eksekusi tool.

    Tidak bertanggung jawab terhadap:

    - Prompt engineering
    - Document retrieval
    - Embedding
    - Vector search
    - Hybrid search
    - LLM invocation
    - LangGraph workflow
    """

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

    # =====================================================
    # METADATA
    # =====================================================

    @property
    def name(
        self,
    ) -> str:
        """
        Tool name.
        """
        return self.NAME

    @property
    def description(
        self,
    ) -> str:
        """
        Tool description.
        """
        return self.DESCRIPTION
    
    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _create_service(
        self,
        *,
        temperature: float | None = None,
    ) -> RAGService:
        """
        Membuat instance RAGService.

        RAGTool tidak menyimpan instance service sebagai state
        agar setiap eksekusi memiliki lifecycle yang terpisah,
        termasuk resource seperti koneksi Weaviate yang
        dikelola oleh RAGService.

        Args:
            temperature:
                Override temperature model apabila diperlukan.

        Returns:
            Instance RAGService.
        """

        logger.debug(
            "Creating RAGService instance."
        )

        return RAGService(
            temperature=temperature,
        )
    
    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def run(
        self,
        **kwargs: Any,
    ) -> str:
        """
        Menjawab pertanyaan menggunakan
        Retrieval-Augmented Generation (RAG).

        Workflow:

            1. Membuat RAGService.
            2. Meneruskan permintaan ke RAGService.
            3. Mengembalikan hasil dari RAGService.
            4. Menutup seluruh resource.

        Args:
            question:
                Pertanyaan pengguna.

            history:
                Riwayat percakapan sebelumnya.

            top_k:
                Jumlah maksimum dokumen yang diambil
                dari vector database.

            temperature:
                Override temperature model.

        Returns:
            Jawaban dari RAGService.
        """

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