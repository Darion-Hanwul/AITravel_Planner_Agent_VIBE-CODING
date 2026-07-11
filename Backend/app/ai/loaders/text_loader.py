from __future__ import annotations

from bs4 import BeautifulSoup
from langchain_core.documents import Document


class TextLoader:
    """
    Loader untuk membersihkan HTML.

    Responsibility:

    - HTML Parsing
    - HTML Cleaning
    - Normalisasi whitespace

    Tidak bertanggung jawab terhadap:

    - HTTP Request
    - Chunking
    - Embedding
    - RAG
    """

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _clean_html(
        self,
        html: str,
    ) -> str:
        """
        Membersihkan HTML menjadi plain text.
        """

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "svg",
            ]
        ):

            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        return " ".join(
            text.split()
        )

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    def transform(
        self,
        document: Document,
    ) -> Document:
        """
        Membersihkan satu LangChain Document.
        """

        return Document(
            page_content=self._clean_html(
                document.page_content,
            ),
            metadata=document.metadata,
        )

    def transform_many(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Membersihkan banyak document.
        """

        return [
            self.transform(
                document,
            )
            for document in documents
        ]