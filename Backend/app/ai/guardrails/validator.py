"""
Input Validator untuk TravelPlannerAgent.

Validator bertanggung jawab memastikan input pengguna
memenuhi standar kualitas sebelum diproses oleh AI.

Responsibility
--------------

- Validasi input kosong
- Validasi panjang input
- Validasi karakter kontrol
- Validasi Unicode
- Validasi kualitas input
- Normalisasi prompt

Tidak bertanggung jawab terhadap

- Prompt Injection Detection
- Moderation
- Tool Calling
- RAG
- LangGraph
- LLM
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.config.settings import settings
from app.core.logger import logger

import unicodedata
import re

@dataclass(slots=True)
class ValidationIssue:
    """
    Merepresentasikan satu hasil validasi.

    Attributes
    ----------
    code:
        Kode unik untuk setiap jenis validasi.

    message:
        Pesan yang dapat ditampilkan kepada user.
    """

    code: str
    message: str

@dataclass(slots=True)
class ValidationResult:
    """
    Hasil validasi input pengguna.
    """

    valid: bool
    normalized_prompt: str

    errors: list[ValidationIssue] = field(
        default_factory=list,
    )

    warnings: list[ValidationIssue] = field(
        default_factory=list,
    )


class InputValidator:
    """
    Validator untuk seluruh input pengguna.

    Validator ini merupakan guardrail pertama
    sebelum prompt diproses oleh AI.

    Seluruh validasi dilakukan secara deterministic
    tanpa bantuan model AI maupun embedding.
    """

    def __init__(self) -> None:
        """
        Inisialisasi validator menggunakan konfigurasi
        dari settings.py.
        """

        self.min_prompt_length = (
            settings.MIN_PROMPT_LENGTH
        )

        self.max_prompt_length = (
            settings.MAX_PROMPT_LENGTH
        )

        self.max_consecutive_whitespace = (
            settings.MAX_CONSECUTIVE_WHITESPACE
        )

        self.max_repeated_characters = (
            settings.MAX_REPEATED_CHARACTERS
        )

        self.max_emoji_count = (
            settings.MAX_EMOJI_COUNT
        )

    # =====================================================
    # PUBLIC
    # =====================================================

    def validate(
        self,
        prompt: str,
    ) -> ValidationResult:
        """
        Memvalidasi prompt pengguna sebelum
        diproses oleh AI.

        Seluruh validasi dilakukan secara
        deterministic tanpa menggunakan
        model AI maupun embedding.

        Args
        ----
        prompt:
            Prompt pengguna.

        Returns
        -------
        ValidationResult
        """

        logger.debug(
            "Starting input validation."
        )

        errors: list[ValidationIssue] = []

        warnings: list[ValidationIssue] = []

        # ==========================================
        # Normalize Prompt
        # ==========================================

        normalized_prompt, normalize_warning = (
            self._normalize_prompt(
                prompt,
            )
        )

        warnings.extend(
            normalize_warning,
        )

        # ==========================================
        # Validation Pipeline
        # ==========================================

        self._check_empty(
            normalized_prompt,
            errors,
        )

        self._check_length(
            normalized_prompt,
            errors,
        )

        self._check_unicode(
            normalized_prompt,
            errors,
        )

        self._check_control_characters(
            normalized_prompt,
            errors,
        )

        self._check_whitespace(
            normalized_prompt,
            warnings,
        )

        self._check_repeated_characters(
            normalized_prompt,
            warnings,
        )

        self._check_emoji_spam(
            normalized_prompt,
            warnings,
        )

        valid = len(errors) == 0

        logger.info(
            "Validation completed | valid={} | errors={} | warnings={}",
            valid,
            len(errors),
            len(warnings),
        )

        return ValidationResult(
            valid=valid,
            normalized_prompt=normalized_prompt,
            errors=errors,
            warnings=warnings,
        )
    
    def is_valid(
        self,
        prompt: str,
    ) -> bool:
        """
        Mengembalikan status validasi saja.

        Berguna apabila caller hanya
        membutuhkan nilai boolean.
        """

        return self.validate(
            prompt,
        ).valid
    
    def normalize(
        self,
        prompt: str,
    ) -> str:
        """
        Mengembalikan prompt yang telah
        dinormalisasi tanpa menjalankan
        seluruh proses validasi.
        """

        normalized, _ = (
            self._normalize_prompt(
                prompt,
            )
        )

        return normalized
    
    # =====================================================
    # PRIVATE
    # =====================================================

    def _check_empty(
        self,
        prompt: str,
        errors: list[ValidationIssue],
    ) -> None:
        """
        Memastikan prompt tidak kosong.

        Args
        ----
        prompt:
            Prompt pengguna.

        errors:
            Daftar error validasi.
        """

        if not prompt.strip():

            errors.append(
                ValidationIssue(
                    code="EMPTY_PROMPT",
                    message="Prompt cannot be empty.",
                )
            )

            logger.warning(
                "Validation failed: empty prompt."
            )

    def _check_length(
        self,
        prompt: str,
        errors: list[ValidationIssue],
    ) -> None:
        """
        Memastikan panjang prompt berada
        dalam batas konfigurasi.

        Args
        ----
        prompt:
            Prompt pengguna.

        errors:
            Daftar error validasi.
        """

        length = len(prompt)

        if length < self.min_prompt_length:

            errors.append(
                ValidationIssue(
                    code="PROMPT_TOO_SHORT",
                    message="Prompt is too short.",
                )
            )
            logger.warning(
                "Validation failed: prompt too short."
            )

        elif length > self.max_prompt_length:

            errors.append(
                ValidationIssue(
                    code="PROMPT_TOO_LONG",
                    message="Prompt exceeds maximum length.",
                )
            )

            logger.warning(
                "Validation failed: prompt too long."
            )

    def _check_unicode(
        self,
        prompt: str,
        errors: list[ValidationIssue],
    ) -> None:
        """
        Memastikan seluruh karakter Unicode
        valid.

        Args
        ----
        prompt:
            Prompt pengguna.

        errors:
            Daftar error validasi.
        """

        try:

            prompt.encode(
                "utf-8",
                errors="strict",
            )

        except UnicodeError:

            errors.append(
                ValidationIssue(
                    code="CONTROL_CHARACTER",
                    message="Control characters detected.",
                )
            )

            logger.warning(
                "Validation failed: invalid unicode."
            )

    def _check_control_characters(
        self,
        prompt: str,
        errors: list[ValidationIssue],
    ) -> None:
        """
        Mendeteksi control character
        selain newline dan tab.

        Karakter seperti:

        \\x00
        \\x01
        \\x08

        akan ditolak.

        Args
        ----
        prompt:
            Prompt pengguna.

        errors:
            Daftar error validasi.
        """

        for character in prompt:

            category = unicodedata.category(
                character,
            )

            if (
                category == "Cc"
                and character not in (
                    "\n",
                    "\t",
                )
            ):

                errors.append(
                    ValidationIssue(
                        code="CONTROL_CHARACTER",
                        message="Control characters detected.",
                    )
                )

                logger.warning(
                    "Validation failed: control character detected."
                )

                return
            
    def _normalize_prompt(
        self,
        prompt: str,
    ) -> tuple[str, list[ValidationIssue]]:
        """
        Membersihkan whitespace yang tidak diperlukan.

        Returns
        -------
        tuple[str, list[str]]

            Prompt yang telah dinormalisasi
            beserta warning yang dihasilkan.
        """

        warnings: list[ValidationIssue] = []

        normalized = re.sub(
            r"\s+",
            " ",
            prompt,
        ).strip()

        if normalized != prompt:

            warnings.append(
                ValidationIssue(
                    code="WHITESPACE_NORMALIZED",
                    message="Prompt whitespace normalized.",
                )
            )

            logger.debug(
                "Prompt whitespace normalized."
            )

        return normalized, warnings
    
    def _check_whitespace(
        self,
        prompt: str,
        warnings: list[ValidationIssue],
    ) -> None:
        """
        Mendeteksi whitespace yang terlalu banyak.
        """

        pattern = (
            rf"\s{{{self.max_consecutive_whitespace},}}"
        )

        if re.search(
            pattern,
            prompt,
        ):

            warnings.append(
                ValidationIssue(
                    code="EXCESSIVE_WHITESPACE",
                    message="Excessive whitespace detected.",
                )
            )

            logger.debug(
                "Excessive whitespace detected."
            )

    def _check_repeated_characters(
        self,
        prompt: str,
        warnings: list[ValidationIssue],
    ) -> None:
        """
        Mendeteksi karakter yang berulang
        secara berlebihan.

        Contoh

        AAAAAAAAAAAAA

        !!!!!!!!!

        ????????
        """

        pattern = (
            rf"(.)\1{{{self.max_repeated_characters},}}"
        )

        if re.search(
            pattern,
            prompt,
        ):

            warnings.append(
                ValidationIssue(
                    code="REPEATED_CHARACTER",
                    message="Repeated characters detected.",
                )
            )

            logger.debug(
                "Repeated characters detected."
            )

    def _check_emoji_spam(
        self,
        prompt: str,
        warnings: list[ValidationIssue],
    ) -> None:
        """
        Mendeteksi jumlah emoji yang
        terlalu banyak.
        """

        emoji_pattern = re.compile(

            "["

            "\U0001F600-\U0001F64F"

            "\U0001F300-\U0001F5FF"

            "\U0001F680-\U0001F6FF"

            "\U0001F700-\U0001F77F"

            "\U0001F780-\U0001F7FF"

            "\U0001F800-\U0001F8FF"

            "\U0001F900-\U0001F9FF"

            "\U0001FA00-\U0001FAFF"

            "]+",

            flags=re.UNICODE,

        )

        emojis = emoji_pattern.findall(
            prompt,
        )

        emoji_count = sum(
            len(item)
            for item in emojis
        )

        if emoji_count > self.max_emoji_count:

            warnings.append(
                ValidationIssue(
                    code="EMOJI_SPAM",
                    message="Emoji spam detected.",
                )
            )

            logger.debug(
                "Emoji spam detected."
            )