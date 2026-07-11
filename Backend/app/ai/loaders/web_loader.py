from __future__ import annotations

import asyncio

import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from app.ai.sources.source import Source
from app.core.logger import logger


class WebLoader:
    """
    Asynchronous Web Loader.

    Bertanggung jawab terhadap:

    - HTTP Request
    - Retry
    - HTML Cleaning
    - Convert menjadi LangChain Document

    Tidak bertanggung jawab terhadap:

    - Chunking
    - Embedding
    - Weaviate
    - RAG
    """

    DEFAULT_HEADERS = {
        "User-Agent": (
            "TravelPlannerAgent/1.0 "
            "(AI Knowledge Indexer)"
        )
    }

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:

        self.timeout = timeout
        self.max_retries = max_retries

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    async def _fetch(
        self,
        client: httpx.AsyncClient,
        url: str,
    ) -> str:
        """
        Mengambil HTML dari sebuah URL.
        """

        last_exception: Exception | None = None

        for attempt in range(
            1,
            self.max_retries + 1,
        ):

            try:

                response = await client.get(
                    url,
                )

                response.raise_for_status()

                logger.info(
                    f"Success fetching: {url}"
                )

                return response.text

            except Exception as exc:

                last_exception = exc

                logger.warning(
                    (
                        f"Retry "
                        f"{attempt}/{self.max_retries} "
                        f"for {url}"
                    )
                )

                await asyncio.sleep(
                    attempt,
                )

        logger.error(
            f"Failed fetching: {url}"
        )

        raise RuntimeError(
            f"Cannot fetch {url}"
        ) from last_exception

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
                "footer",
                "header",
                "nav",
                "noscript",
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

    def _to_document(
        self,
        source: Source,
        url: str,
        text: str,
    ) -> Document:
        """
        Mengubah hasil crawling menjadi LangChain Document.
        """

        return Document(
            page_content=text,
            metadata={
                "source": source.name,
                "category": source.category,
                "url": url,
            },
        )

    async def _load_url(
        self,
        client: httpx.AsyncClient,
        source: Source,
        url: str,
    ) -> Document:

        html = await self._fetch(
            client,
            url,
        )

        return Document(
            page_content=html,
            metadata={
                "source": source.name,
                "category": source.category,
                "url": url,
            },
        )

    # =====================================================
    # PUBLIC METHODS
    # =====================================================

    async def load(
        self,
        source: Source,
    ) -> list[Document]:
        """
        Melakukan crawling seluruh URL
        pada sebuah Source secara asynchronous.
        """

        headers = (
            source.headers
            if source.headers
            else self.DEFAULT_HEADERS
        )

        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers=headers,
        ) as client:

            tasks = [
                self._load_url(
                    client,
                    source,
                    url,
                )
                for url in source.get_urls()
            ]

            return await asyncio.gather(
                *tasks,
            )