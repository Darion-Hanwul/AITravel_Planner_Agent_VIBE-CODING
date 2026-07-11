from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Source:
    """
    Representasi satu knowledge source.

    Source digunakan sebagai konfigurasi metadata
    untuk proses crawling dan indexing.

    Attributes:
        name:
            Nama source.

        category:
            Kategori knowledge.

        base_url:
            Base URL website.

        urls:
            Daftar endpoint yang akan di-crawl.

        enabled:
            Menentukan apakah source aktif.

        description:
            Deskripsi singkat source.
    """

    name: str

    category: str

    base_url: str

    urls: list[str]

    enabled: bool = True

    description: str = ""

    headers: dict[str, str] = field(
        default_factory=dict,
    )

    timeout: int = 30

    def get_urls(self) -> list[str]:
        """
        Menghasilkan daftar URL lengkap.

        Returns:
            List URL lengkap.
        """

        return [
            self.base_url.rstrip("/") + "/" + url.lstrip("/")
            for url in self.urls
        ]