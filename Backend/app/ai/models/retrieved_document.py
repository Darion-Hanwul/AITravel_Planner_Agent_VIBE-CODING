from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievedDocument:
    """
    Representasi document hasil retrieval dari Vector Database.

    Object ini digunakan sebagai media pertukaran data
    antar AI Service, seperti:

    - RetrieverService
    - RAGService
    - PromptBuilder
    - LangGraph

    Attributes:
        content:
            Isi dokumen.

        metadata:
            Metadata dokumen.

        score:
            Similarity score hasil retrieval.
    """

    content: str

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    score: float = 0.0