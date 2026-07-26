from __future__ import annotations

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from langchain_core.documents import Document

from app.config.settings import settings


class ChunkLoader:
    """
    Loader untuk melakukan document chunking.

    Responsibility:

    - Split LangChain Document
    - Split Text
    - Menjaga metadata

    Tidak bertanggung jawab terhadap:

    - HTML Parsing
    - Embedding
    - Weaviate
    - RAG
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        """
        Initialize ChunkLoader.
        """

        self.chunk_size = (
            chunk_size
            or settings.CHUNK_SIZE
        )

        self.chunk_overlap = (
            chunk_overlap
            or settings.CHUNK_OVERLAP
        )

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    "? ",
                    "! ",
                    "; ",
                    ", ",
                    " ",
                    "",
                ],
                length_function=len,
                add_start_index=True,
                keep_separator=False,
            )
        )

    def split_document(
        self,
        document: Document,
    ) -> list[Document]:
        """
        Split satu document menjadi beberapa chunk.

        Args:
            document:
                LangChain document.

        Returns:
            List chunk document.
        """

        return self.splitter.split_documents(
            [document],
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split banyak document menjadi chunk.

        Args:
            documents:
                List LangChain document.

        Returns:
            Seluruh chunk document.
        """

        return self.splitter.split_documents(
            documents,
        )