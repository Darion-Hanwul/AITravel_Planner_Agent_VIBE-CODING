from __future__ import annotations

from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass(slots=True)
class EmbeddedDocument:

    document: Document

    embedding: list[float]