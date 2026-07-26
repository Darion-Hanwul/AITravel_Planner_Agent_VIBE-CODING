from __future__ import annotations

import logging
from typing import Any
from app.config.settings import settings

logger = logging.getLogger("app.ai.memory.conversation")


class ConversationMemory:
 
    def __init__(self) -> None:

        self._storage: dict[str, list[dict[str, str]]] = {}
        
        # Ambil batasan max token/history dari settings (Prinsip 4)
        self._max_history: int = getattr(settings, "MAX_CONVERSATION_HISTORY", 10)

    def add_message(self, session_id: str, role: str, content: str) -> None:

        if not session_id:
            logger.warning("[ConversationMemory] Menolak menyimpan pesan karena session_id kosong.")
            return

        if session_id not in self._storage:
            self._storage[session_id] = []

        self._storage[session_id].append({"role": role, "content": content})
        logger.debug(f"[ConversationMemory] Pesan [{role}] berhasil ditambahkan ke sesi '{session_id}'.")

        # Sliding Window: Batasi kapasitas riwayat agar tidak membengkak (Prinsip 24)
        if len(self._storage[session_id]) > self._max_history * 2:  # *2 karena sepasang user-assistant
            self._storage[session_id] = self._storage[session_id][-self._max_history * 2:]
            logger.debug(f"[ConversationMemory] Melakukan trim histori sesi '{session_id}' ke batas maksimum.")

    def get_history_as_list(self, session_id: str) -> list[str]:

        session_messages = self._storage.get(session_id, [])
        formatted_history: list[str] = []

        for msg in session_messages:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            formatted_history.append(f"{role_label}: {msg['content']}")

        return formatted_history

    def clear(self, session_id: str) -> None:

        if session_id in self._storage:
            del self._storage[session_id]
            logger.info(f"[ConversationMemory] Histori untuk sesi '{session_id}' berhasil dibersihkan.")