from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetrievedDocument:
    
    content: str

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    score: float = 0.0