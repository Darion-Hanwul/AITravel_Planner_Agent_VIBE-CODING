"""
Output Filter Guard untuk TravelPlannerAgent.

Mencegah kebocoran data sensitif, informasi internal sistem, 
dan teks mentah dari tool calling sebelum dikirim ke pengguna akhir.

Responsibility
--------------
- Menghapus ekspresi reguler yang mencerminkan instruksi internal (System Prompts Leakage).
- Membersihkan jejak metadata internal agen atau nama fungsi internal.
- Menyensor data sensitif (PII) seperti nomor kartu kredit atau token/API Key yang tidak sengaja tercetak.
- Memastikan respons akhir ramah pengguna dan bersih dari format sintaksis internal.

Tidak bertanggung jawab terhadap
- Input Validation
- Prompt Injection Detection
- Moderation Check (Input-level)
- Mengubah struktur data objek respons (hanya menyaring konten teks).
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re

from app.config.settings import settings
from app.core.logger import logger


@dataclass(slots=True)
class OutputFilterResult:
    """Hasil dari proses penyaringan output teks LLM."""
    clean_text: str
    is_modified: bool
    filtered_categories: list[str] = field(default_factory=list)


class OutputFilterGuard:
    """
    Sanitizer otomatis untuk menyaring output teks dari LLM 
    sebelum dikirimkan ke lapisan API / user interface.
    """

    def __init__(self) -> None:
        """Inisialisasi regex pattern untuk pembersihan output."""
        logger.info("Initializing OutputFilterGuard.")
        
        # 1. Pola Kebocoran Prompt Internal / System Prompt Triggers
        self.system_prompt_patterns = [
            re.compile(r"(you are a personal travel assistant|your task is to help|follow clean architecture)", re.IGNORECASE),
            re.compile(r"(system prompt|instruksi internal|core instructions|agent role:)", re.IGNORECASE),
            re.compile(r"(thought process|mata rantai pemikiran|reasoning path):?.*?\n", re.IGNORECASE)
        ]

        # 2. Pola Kebocoran Data Sensitif (PII & Secrets)
        self.sensitive_data_patterns = {
            "API_KEY": re.compile(r"(aiza[0-9A-Za-z-_]{35}|sk-[a-zA-Z0-9]{48}|ghp_[a-zA-Z0-9]{36})"),
            "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
            "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        }

        # 3. Pola Kebocoran Data Mentah Tool / Agen internal
        self.tool_leakage_patterns = [
            re.compile(r"<\s*tool_call\s*>.*?<\s*/\s*tool_call\s*>", re.DOTALL | re.IGNORECASE),
            re.compile(r"\{\s*\"tool\"\s*:\s*\".*?\"\s*,\s*\"args\"\s*:\s*\{.*?\}\s*\}", re.DOTALL),
            re.compile(r"(executing tool|calling api|response from database|raw json response):?", re.IGNORECASE)
        ]

        logger.info("OutputFilterGuard patterns compiled successfully.")

    def filter(self, raw_text: str) -> OutputFilterResult:
        """
        Menyaring konten teks mentah dari LLM dari segala bentuk kebocoran sistem.
        
        Args:
            raw_text: Teks mentah yang dihasilkan oleh LLM/Agent workflow.
            
        Returns:
            OutputFilterResult berisi teks bersih dan status modifikasi.
        """
        if not raw_text or not raw_text.strip():
            return OutputFilterResult(clean_text=raw_text, is_modified=False)

        logger.info("Executing output filtration process.")
        current_text = raw_text
        modified_categories: list[str] = []

        # Step 1: Bersihkan Kebocoran Prompt Sistem / Pemikiran Internal Agen
        for pattern in self.system_prompt_patterns:
            if pattern.search(current_text):
                current_text = pattern.sub("", current_text)
                if "SYSTEM_PROMPT" not in modified_categories:
                    modified_categories.append("SYSTEM_PROMPT")

        # Step 2: Bersihkan Struktur Pemanggilan Tool Mentah (JSON / XML tags dari LLM)
        for pattern in self.tool_leakage_patterns:
            if pattern.search(current_text):
                current_text = pattern.sub("", current_text)
                if "TOOL_METADATA" not in modified_categories:
                    modified_categories.append("TOOL_METADATA")

        # Step 3: Sensor Data Sensitif (PII / Kredensial rahasia)
        for category, pattern in self.sensitive_data_patterns.items():
            if pattern.search(current_text):
                current_text = pattern.sub("[REDACTED]", current_text)
                modified_categories.append(category)

        # Post-processing: Bersihkan spasi berlebih atau baris kosong akibat pembersihan regex
        current_text = re.sub(r'\n\s*\n', '\n\n', current_text).strip()

        is_modified = len(modified_categories) > 0
        if is_modified:
            logger.warning(f"Output filter modified the text. Filtered items: {modified_categories}")
        else:
            logger.info("Output text passed safety filters without any modifications.")

        return OutputFilterResult(
            clean_text=current_text,
            is_modified=is_modified,
            filtered_categories=modified_categories
        )

    def __repr__(self) -> str:
        """Representasi string resmi untuk objek OutputFilterGuard."""
        return "OutputFilterGuard(active_filters=3)"