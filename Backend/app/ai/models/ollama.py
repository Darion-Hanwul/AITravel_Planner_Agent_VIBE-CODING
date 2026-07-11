"""
Factory untuk seluruh model Ollama yang digunakan
oleh TravelPlannerAgent.

Seluruh AI component harus mengambil model
melalui class ini agar konfigurasi berada
di satu tempat.
"""

from langchain_ollama import (
    ChatOllama,
    OllamaEmbeddings,
)
from app.config.settings import settings


class OllamaModel:

    CHAT_MODEL = settings.OLLAMA_MODEL

    EMBEDDING_MODEL = settings.OLLAMA_EMBED_MODEL

    BASE_URL = settings.OLLAMA_BASE_URL

    TEMPERATURE = 0.2
    @classmethod
    def get_chat_model(
        cls,
        temperature: float | None = None,
    ) -> ChatOllama:
        """
        Membuat ChatOllama instance.

        Args:
            temperature:
                Override temperature bawaan.

        Returns:
            ChatOllama
        """

        return ChatOllama(
            model=cls.CHAT_MODEL,
            base_url=cls.BASE_URL,
            temperature=(
                temperature
                if temperature is not None
                else cls.TEMPERATURE
            ),
        )

    @classmethod
    def get_embedding_model(
        cls,
    ) -> OllamaEmbeddings:
        """
        Membuat Ollama Embedding Model.

        Returns:
            OllamaEmbeddings
        """

        return OllamaEmbeddings(
            model=cls.EMBEDDING_MODEL,
            base_url=cls.BASE_URL,
        )