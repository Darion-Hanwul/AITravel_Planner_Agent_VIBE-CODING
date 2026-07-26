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

        return OllamaEmbeddings(
            model=cls.EMBEDDING_MODEL,
            base_url=cls.BASE_URL,
        )