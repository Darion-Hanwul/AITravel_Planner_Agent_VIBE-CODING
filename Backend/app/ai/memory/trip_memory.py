from __future__ import annotations

import logging
from typing import Any, TypedDict

logger = logging.getLogger("app.ai.memory.trip")
class TripProfile(TypedDict, total=False):

    destination: str
    travel_dates: str
    duration_days: int
    budget_tier: str  # backpacker, moderate, luxury
    user_nationality: str
    preferences: list[str]  # e.g., ["no seafood", "museum lover"]
    excluded_activities: list[str]
class TripMemory:

    def __init__(self) -> None:
        # In-memory storage. Dapat digantikan oleh persistent database pada database layer (Prinsip 2).
        self._profiles: dict[str, TripProfile] = {}

    def get_profile(self, session_id: str) -> TripProfile:
        """
        Mendapatkan profil preferensi perjalanan saat ini untuk sesi tertentu.
        """
        if session_id not in self._profiles:
            # Sediakan default values yang aman
            self._profiles[session_id] = {
                "destination": "",
                "travel_dates": "",
                "duration_days": 1,
                "budget_tier": "moderate",
                "user_nationality": "indonesia",
                "preferences": [],
                "excluded_activities": []
            }
        return self._profiles[session_id]

    def update_profile(self, session_id: str, updates: dict[str, Any]) -> TripProfile:
        current_profile = self.get_profile(session_id)
        
        # Lakukan pembaruan secara selektif
        for key, value in updates.items():
            if key in current_profile:
                if isinstance(current_profile[key], list) and isinstance(value, list):
                    # Gabungkan list tanpa duplikasi (misal preferensi baru)
                    current_profile[key] = list(set(current_profile[key] + value))  # type: ignore
                else:
                    current_profile[key] = value  # type: ignore
        
        self._profiles[session_id] = current_profile
        logger.info(f"[TripMemory] Profil perjalanan untuk sesi '{session_id}' berhasil diperbarui: {updates}")
        return current_profile

    def clear_profile(self, session_id: str) -> None:
        """
        Menghapus draf data profil perjalanan.
        """
        if session_id in self._profiles:
            del self._profiles[session_id]
            logger.info(f"[TripMemory] Profil perjalanan untuk sesi '{session_id}' telah dihapus.")