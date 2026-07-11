from __future__ import annotations

from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass(slots=True)
class EmbeddedDocument:
    """
    Representasi document yang telah memiliki vector embedding.

    Object ini digunakan sebagai media pertukaran data
    antar AI Service, seperti:

    - EmbeddingService
    - IndexingService
    - RetrieverService

    Attributes:
        document:
            LangChain Document.

        embedding:
            Vector embedding hasil model embedding.
    """

    document: Document

    embedding: list[float]