from __future__ import annotations

from dataclasses import dataclass, field
from app.config.settings import settings


@dataclass(slots=True, frozen=True)
class Source:

    name: str
    category: str
    base_url: str
    urls: list[str]
    enabled: bool = True
    description: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    # Menarik nilai default timeout dari settings.py demi kepatuhan Prinsip 4
    timeout: int = field(default_factory=lambda: getattr(settings, "CRAWLER_TIMEOUT", 30))

    def get_urls(self) -> list[str]:

        return [
            self.base_url.rstrip("/") + "/" + url.lstrip("/")
            for url in self.urls
        ]