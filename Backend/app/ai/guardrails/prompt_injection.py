from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import re
import numpy as np

from app.ai.services.embedding_service import (
    EmbeddingService,
)
from app.config.settings import settings
from app.core.logger import logger


class RiskLevel(str, Enum):
    """
    Tingkat risiko Prompt Injection.

    LOW
        Tidak ditemukan indikasi.

    MEDIUM
        Terdapat indikasi ringan.

    HIGH
        Sangat mencurigakan.

    CRITICAL
        Hampir dipastikan merupakan
        Prompt Injection.
    """

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


@dataclass(slots=True)
class InjectionIssue:
    """
    Merepresentasikan satu hasil deteksi
    Prompt Injection.

    Attributes
    ----------
    code:
        Kode unik jenis deteksi.

    message:
        Penjelasan hasil deteksi.

    score:
        Nilai kontribusi terhadap total
        risk score.
    """

    code: str

    message: str

    score: float


@dataclass(slots=True)
class InjectionResult:
    """
    Hasil pemeriksaan Prompt Injection.

    Attributes
    ----------
    allowed:
        Menunjukkan apakah prompt boleh
        diproses oleh AI.

    score:
        Total risk score.

    risk_level:
        Tingkat risiko Prompt Injection.

    issues:
        Daftar hasil deteksi.

    matched_patterns:
        Daftar regex atau keyword yang
        berhasil terdeteksi.
    """

    allowed: bool

    score: float

    risk_level: RiskLevel

    issues: list[InjectionIssue] = field(
        default_factory=list,
    )

    matched_patterns: list[str] = field(
        default_factory=list,
    )

@dataclass(slots=True)
class ExampleEmbedding:
    """
    Menyimpan pasangan antara contoh
    Prompt Injection dan embedding-nya.

    Digunakan oleh Embedding Detection
    agar dapat mengetahui contoh mana
    yang paling mirip dengan prompt pengguna.
    """

    text: str

    embedding: list[float]

class PromptInjectionGuard:
    """
    Guard untuk mendeteksi Prompt Injection.

    Guard ini merupakan lapisan keamanan kedua
    setelah Input Validator.

    Seluruh deteksi dilakukan menggunakan
    Hybrid Detection yang terdiri dari:

    - Regex Detection
    - Keyword Detection
    - Embedding Similarity
    - Weighted Scoring

    Guard ini tidak menggunakan LLM sehingga
    proses deteksi bersifat deterministic,
    cepat, dan konsisten.
    """

    def __init__(
        self,
    ) -> None:
        """
        Inisialisasi Prompt Injection Guard.
        """

        logger.info(
            "Initializing PromptInjectionGuard."
        )

        # ==========================================
        # Embedding
        # ==========================================

        self.embedding_service = (
            EmbeddingService()
        )

        # ==========================================
        # Threshold
        # ==========================================

        self.threshold = (
            settings.PROMPT_INJECTION_THRESHOLD
        )

        self.similarity_threshold = (
            settings.PROMPT_INJECTION_SIMILARITY_THRESHOLD
        )

        self.regex_early_stop = (
            settings.PROMPT_INJECTION_REGEX_EARLY_STOP
        )

        self.combined_early_stop = (
            settings.PROMPT_INJECTION_COMBINED_EARLY_STOP
        )
        # ==========================================
        # Weight
        # ==========================================

        self.regex_weight = (
            settings.PROMPT_INJECTION_REGEX_WEIGHT
        )

        self.keyword_weight = (
            settings.PROMPT_INJECTION_KEYWORD_WEIGHT
        )

        self.embedding_weight = (
            settings.PROMPT_INJECTION_EMBEDDING_WEIGHT
        )

        # ==========================================
        # Prompt Examples
        # ==========================================

        self.examples_path = Path(
            settings.PROMPT_INJECTION_EXAMPLES_FILE,
        )

        self.prompt_examples = (
            self._load_prompt_examples()
        )

        # ==========================================
        # Embedding Cache
        # ==========================================

        self.example_embeddings = (
            self._build_example_embeddings()
        )

        # ==========================================
        # Detection Rules
        # ==========================================

        self.regex_patterns = (
            self._load_regex_patterns()
        )

        self.keyword_groups = (
            self._load_keyword_groups()
        )

        self.keyword_patterns = (
            self._compile_keyword_patterns()
        )

        logger.info(
            "PromptInjectionGuard initialized successfully."
        )

    # =====================================================
    # PRIVATE INITIALIZATION
    # =====================================================

    def _load_prompt_examples(
        self,
    ) -> list[str]:
        """
        Membaca dataset Prompt Injection.

        Returns
        -------
        list[str]
        """

        if not self.examples_path.exists():

            logger.warning(
                "Prompt injection examples file not found: {}",
                self.examples_path,
            )

            return []

        examples: list[str] = []

        with self.examples_path.open(
            mode="r",
            encoding="utf-8",
        ) as file:

            for line in file:

                text = line.strip()

                if not text:
                    continue

                if text.startswith("#"):
                    continue

                examples.append(
                    text,
                )

        logger.info(
            "Loaded {} prompt injection examples.",
            len(examples),
        )

        return examples

    def _build_example_embeddings(
        self,
    ) -> list[ExampleEmbedding]:
        """
        Membuat embedding seluruh contoh
        Prompt Injection.

        Embedding hanya dibuat sekali saat
        inisialisasi agar tidak membebani
        setiap request.

        Returns
        -------
        list[list[float]]
        """

        if not self.prompt_examples:

            return []

        logger.info(
            "Building prompt injection embeddings."
        )

        embeddings = (
            self.embedding_service.embed_texts(
                self.prompt_examples,
            )
        )

        examples: list[
            ExampleEmbedding
        ] = []

        for text, embedding in zip(
            self.prompt_examples,
            embeddings,
            strict=True,
        ):

            examples.append(
                ExampleEmbedding(
                    text=text,
                    embedding=embedding,
                )
            )

        logger.info(
            "Prompt injection embeddings created: {}",
            len(examples),
        )

        return examples

    def _load_regex_patterns(
        self,
    ) -> dict[str, tuple[re.Pattern[str], float]]:
        """
        Memuat seluruh regex pattern
        Prompt Injection.

        Setiap pattern memiliki weight
        yang akan digunakan pada
        Weighted Scoring Engine.

        Returns
        -------
        dict[str, tuple[str, float]]
        """

        return {

        # =====================================
        # Instruction Override
        # =====================================

        "IGNORE_INSTRUCTION": (
            re.compile(
                r"ignore\s+.*instruction",
                re.IGNORECASE,
            ),
            0.45,
        ),

        "FORGET_CONTEXT": (
            re.compile(
                r"forget\s+.*(instruction|context|above|previous)",
                re.IGNORECASE,
            ),
            0.40,
        ),

        "DISREGARD_RULES": (
            re.compile(
                r"disregard\s+.*(rule|instruction|context)",
                re.IGNORECASE,
            ),
            0.45,
        ),

        "OVERRIDE_BEHAVIOR": (
            re.compile(
                r"override\s+.*(system|instruction|behavior)",
                re.IGNORECASE,
            ),
            0.50,
        ),

        # =====================================
        # System Prompt Disclosure
        # =====================================

        "SYSTEM_PROMPT": (
            re.compile(
                r"system\s+prompt",
                re.IGNORECASE,
            ),
            0.35,
        ),

        "DEVELOPER_PROMPT": (
            re.compile(
                r"developer\s+prompt",
                re.IGNORECASE,
            ),
            0.35,
        ),

        "HIDDEN_PROMPT": (
            re.compile(
                r"hidden\s+prompt",
                re.IGNORECASE,
            ),
            0.35,
        ),

        "INITIAL_PROMPT": (
            re.compile(
                r"initial\s+prompt",
                re.IGNORECASE,
            ),
            0.30,
        ),

        # =====================================
        # Prompt Disclosure
        # =====================================

        "REVEAL_SYSTEM_PROMPT": (
            re.compile(
                r"(reveal|show|display|print|expose)\s+.*"
                r"(system\s+prompt|developer\s+prompt|hidden\s+prompt|internal\s+prompt)",
                re.IGNORECASE,
            ),
            0.40,
        ),

        "REPEAT_SYSTEM_PROMPT": (
            re.compile(
                r"(repeat|output|return)\s+.*"
                r"(system\s+prompt|developer\s+prompt|hidden\s+prompt)",
                re.IGNORECASE,
            ),
            0.45,
        ),

        # =====================================
        # Jailbreak
        # =====================================

        "JAILBREAK": (
            re.compile(
                r"jailbreak",
                re.IGNORECASE,
            ),
            0.60,
        ),

        "BYPASS": (
            re.compile(
                r"bypass\s+.*",
                re.IGNORECASE,
            ),
            0.55,
        ),

        "UNRESTRICTED": (
            re.compile(
                r"unrestricted",
                re.IGNORECASE,
            ),
            0.45,
        ),

        # =====================================
        # Role Override
        # =====================================

        "ACT_AS": (
            re.compile(
                r"act\s+as\s+.*",
                re.IGNORECASE,
            ),
            0.40,
        ),

        "PRETEND": (
            re.compile(
                r"pretend\s+.*",
                re.IGNORECASE,
            ),
            0.30,
        ),

        "ROLEPLAY": (
            re.compile(
                r"roleplay\s+.*",
                re.IGNORECASE,
            ),
            0.25,
        ),

        # =====================================
        # Tool Disclosure
        # =====================================

        "TOOLS_DISCLOSURE": (
            re.compile(
                r"(show|reveal|display|list|print)\s+.*"
                r"(internal\s+tool|tool\s+schema|tool\s+list|available\s+tools)",
                re.IGNORECASE,
            ),
            0.40,
        ),

        # =====================================
        # Memory Disclosure
        # =====================================

        "MEMORY": (
            re.compile(
                r"(memory|conversation|history)\s+.*",
                re.IGNORECASE,
            ),
            0.30,
        ),
    }

    def _compile_keyword_patterns(
        self,
    ) -> dict[str, list[re.Pattern[str]]]:
        """
        Meng-compile seluruh keyword menjadi
        regex pattern.

        Pattern dibuat satu kali saat
        inisialisasi agar tidak perlu
        melakukan compile pada setiap request.

        Returns
        -------
        dict[str, list[re.Pattern[str]]]
        """

        compiled: dict[
            str,
            list[re.Pattern[str]]
        ] = {}

        for code, (
            keywords,
            _,
        ) in self.keyword_groups.items():

            compiled[code] = [

                re.compile(
                    rf"\b{re.escape(keyword)}\b",
                    re.IGNORECASE,
                )

                for keyword in keywords

            ]

        return compiled

    def _load_keyword_groups(
        self,
    ) -> dict[str, tuple[list[str], float]]:
        """
        Memuat kelompok keyword Prompt Injection.

        Setiap kelompok memiliki bobot
        yang akan digunakan pada
        Weighted Scoring.

        Returns
        -------
        dict[str, tuple[list[str], float]]
        """

        return {

            # =====================================
            # Instruction Override
            # =====================================

            "IGNORE": (
                [
                    "ignore",
                    "disregard",
                    "forget",
                    "override",
                    "replace",
                    "skip",
                ],
                0.30,
            ),

            # =====================================
            # System Prompt
            # =====================================

            "SYSTEM_PROMPT": (
                [
                    "system prompt",
                    "developer prompt",
                    "hidden prompt",
                    "initial prompt",
                    "internal prompt",
                ],
                0.35,
            ),

            # =====================================
            # Reveal
            # =====================================

            "DISCLOSURE": (
                [
                    "reveal",
                    "show",
                    "display",
                    "print",
                    "expose",
                    "output",
                ],
                0.25,
            ),

            # =====================================
            # Jailbreak
            # =====================================

            "JAILBREAK": (
                [
                    "jailbreak",
                    "bypass",
                    "unrestricted",
                    "dan mode",
                    "developer mode",
                ],
                0.45,
            ),

            # =====================================
            # Role Override
            # =====================================

            "ROLE": (
                [
                    "act as",
                    "pretend",
                    "roleplay",
                    "simulate",
                ],
                0.25,
            ),

            # =====================================
            # Internal
            # =====================================

            # =====================================
            # Internal Access
            # =====================================

            "INTERNAL": (
                [
                    "internal tool",
                    "tool schema",
                    "tool list",
                    "hidden tool",
                    "internal api",
                    "internal instruction",
                    "conversation history",
                    "developer prompt",
                    "system prompt",
                    "hidden prompt",
                    "api key",
                    "access token",
                    "secret key",
                    "private key",
                ],
                0.35,
            ),
        }
    
    # =====================================================
    # PUBLIC
    # =====================================================

    def check(
        self,
        prompt: str,
    ) -> InjectionResult:
        """
        Melakukan pemeriksaan Prompt Injection.

        Seluruh engine akan dijalankan kemudian
        menghasilkan satu keputusan akhir.

        Args
        ----
        prompt:
            Prompt pengguna.

        Returns
        -------
        InjectionResult
        """

        logger.debug(
            "Starting prompt injection detection."
        )

        issues: list[InjectionIssue] = []

        matched_patterns: list[str] = []

        # ==========================================
        # Regex Detection
        # ==========================================

        regex_score = self._regex_detection(
            prompt=prompt,
            issues=issues,
            matched_patterns=matched_patterns,
        )

        # ==========================================
        # Early Stop (Regex)
        # ==========================================

        if regex_score >= self.regex_early_stop:

            logger.warning(
                "Early stop triggered by regex detection."
            )

            return InjectionResult(
                allowed=False,
                score=1.0,
                risk_level=RiskLevel.CRITICAL,
                issues=issues,
                matched_patterns=matched_patterns,
            )

        # ==========================================
        # Keyword Detection
        # ==========================================

        keyword_score = self._keyword_detection(
            prompt=prompt,
            issues=issues,
            matched_patterns=matched_patterns,
        )

        combined_score = (

            regex_score
            * self.regex_weight

            +

            keyword_score
            * self.keyword_weight

        )

        if combined_score >= self.combined_early_stop:

            logger.warning(
                "Early stop triggered by regex + keyword."
            )

            total_score = combined_score

            return InjectionResult(

                allowed=False,

                score=total_score,

                risk_level=self._calculate_risk_level(
                    total_score,
                ),

                issues=issues,

                matched_patterns=matched_patterns,
            )
        
        embedding_score = (
            self._embedding_detection(
                prompt=prompt,
                issues=issues,
            )
        )

        total_score = self._calculate_score(
            regex_score=regex_score,
            keyword_score=keyword_score,
            embedding_score=embedding_score,
        )

        risk_level = self._calculate_risk_level(
            total_score,
        )

        allowed = self._make_decision(
            total_score,
        )

        logger.info(
            "Prompt Injection Detection completed | "
            "allowed={} | score={:.3f} | risk={}",
            allowed,
            total_score,
            risk_level.value,
        )

        return InjectionResult(
            allowed=allowed,
            score=total_score,
            risk_level=risk_level,
            issues=issues,
            matched_patterns=matched_patterns,
        )
    
    def is_safe(
        self,
        prompt: str,
    ) -> bool:
        """
        Memeriksa apakah prompt aman
        untuk diproses.

        Method ini berguna apabila caller
        hanya membutuhkan nilai boolean.

        Args
        ----
        prompt:
            Prompt pengguna.

        Returns
        -------
        bool
        """

        return self.check(
            prompt,
        ).allowed
    
    def risk_score(
        self,
        prompt: str,
    ) -> float:
        """
        Mengembalikan nilai risk score.

        Args
        ----
        prompt:
            Prompt pengguna.

        Returns
        -------
        float
        """

        return self.check(
            prompt,
        ).score

    def risk_level(
        self,
        prompt: str,
    ) -> RiskLevel:
        """
        Mengembalikan tingkat risiko
        Prompt Injection.

        Args
        ----
        prompt:
            Prompt pengguna.

        Returns
        -------
        RiskLevel
        """

        return self.check(
            prompt,
        ).risk_level
    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _calculate_score(
        self,
        *,
        regex_score: float,
        keyword_score: float,
        embedding_score: float,
    ) -> float:
        """
        Menghitung total risk score menggunakan
        Weighted Scoring.

        Returns
        -------
        float

            Total score antara
            0.0 hingga 1.0.
        """

        logger.debug(
            "Calculating weighted risk score."
        )

        total_score = (

            regex_score
            * self.regex_weight

            +

            keyword_score
            * self.keyword_weight

            +

            embedding_score
            * self.embedding_weight

        )

        total_score = max(
            0.0,
            min(
                total_score,
                1.0,
            ),
        )

        logger.debug(
            (
                "Weighted score | "
                "regex={:.3f}, "
                "keyword={:.3f}, "
                "embedding={:.3f}, "
                "total={:.3f}"
            ),
            regex_score,
            keyword_score,
            embedding_score,
            total_score,
        )

        return total_score

    def _calculate_risk_level(
        self,
        score: float,
    ) -> RiskLevel:
        """
        Menentukan tingkat risiko
        berdasarkan total score.

        Returns
        -------
        RiskLevel
        """

        if score >= 0.90:

            return RiskLevel.CRITICAL

        if score >= 0.70:

            return RiskLevel.HIGH

        if score >= 0.40:

            return RiskLevel.MEDIUM

        return RiskLevel.LOW
    
    def _make_decision(
        self,
        score: float,
    ) -> bool:
        """
        Menentukan apakah prompt
        boleh diproses.

        Returns
        -------
        bool
        """

        allowed = (
            score
            < self.threshold
        )

        logger.debug(
            (
                "Prompt decision | "
                "score={:.3f}, "
                "threshold={:.3f}, "
                "allowed={}"
            ),
            score,
            self.threshold,
            allowed,
        )

        return allowed
    # =====================================================
    # DETECTION ENGINES
    # =====================================================

    def _regex_detection(
        self,
        *,
        prompt: str,
        issues: list[InjectionIssue],
        matched_patterns: list[str],
    ) -> float:
        """
        Regex Detection Engine.

        Mendeteksi Prompt Injection
        menggunakan Regular Expression.

        Returns
        -------
        float

            Regex risk score.
        """

        logger.debug(
            "Running regex detection."
        )

        total_score = 0.0

        prompt = prompt.lower()

        for code, (
            pattern,
            weight,
        ) in self.regex_patterns.items():

            if pattern.search(prompt):

                matched_patterns.append(
                    code,
                )

                issues.append(
                    InjectionIssue(
                        code=code,
                        message=(
                            f"Regex pattern detected: {code}"
                        ),
                        score=weight,
                    )
                )

                total_score += weight

                logger.debug(
                    "Regex matched: {}",
                    code,
                )

        return min(
            total_score,
            1.0,
        )
    
    def _keyword_detection(
        self,
        *,
        prompt: str,
        issues: list[InjectionIssue],
        matched_patterns: list[str],
    ) -> float:
        """
        Keyword Detection Engine.

        Mendeteksi Prompt Injection
        menggunakan keyword matching.

        Returns
        -------
        float

            Keyword risk score.
        """

        logger.debug(
            "Running keyword detection."
        )

        prompt = prompt.lower()

        total_score = 0.0

        for code, (
            keywords,
            weight,
        ) in self.keyword_groups.items():

            found_keywords: list[str] = []

            patterns = self.keyword_patterns[
                code
            ]

            for keyword, pattern in zip(
                keywords,
                patterns,
                strict=True,
            ):

                if pattern.search(prompt):

                    found_keywords.append(
                        keyword,
                    )

            if found_keywords:

                matched_patterns.extend(
                    found_keywords,
                )

                issues.append(
                    InjectionIssue(
                        code=code,
                        message=(
                            f"Detected keyword group: {code}"
                        ),
                        score=weight,
                    )
                )

                total_score += weight

                logger.debug(
                    "Keyword group matched: {} | keywords={}",
                    code,
                    ", ".join(found_keywords),
                )

            logger.debug(
                "Keyword group matched: {} | keywords={}",
                code,
                ", ".join(found_keywords),
            )

        return min(
            total_score,
            1.0,
        )
    
    def _cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:
        """
        Menghitung Cosine Similarity antara dua
        embedding vector menggunakan NumPy.

        Returns
        -------
        float

            Nilai similarity antara
            0.0 hingga 1.0.
        """

        if (
            not vector_a
            or not vector_b
            or len(vector_a) != len(vector_b)
        ):
            return 0.0

        a = np.asarray(
            vector_a,
            dtype=np.float32,
        )

        b = np.asarray(
            vector_b,
            dtype=np.float32,
        )

        denominator = (
            np.linalg.norm(a)
            * np.linalg.norm(b)
        )

        if denominator == 0.0:
            return 0.0

        similarity = float(
            np.dot(a, b) / denominator
        )

        return similarity
        
    def _embedding_detection(
        self,
        *,
        prompt: str,
        issues: list[InjectionIssue],
    ) -> float:
        """
        Embedding Similarity Engine.

        Mendeteksi Prompt Injection
        menggunakan semantic similarity.

        Returns
        -------
        float
        """

        logger.debug(
            "Running embedding detection."
        )

        if not self.example_embeddings:
            return 0.0

        try:

            query_embedding = (
                self.embedding_service.embed_text(
                    prompt,
                )
            )

        except Exception as exception:

            logger.exception(
                "Embedding detection failed: {}",
                exception,
            )

            return 0.0

        highest_similarity = 0.0

        best_example: str | None = None

        for example in self.example_embeddings:

            try:

                similarity = self._cosine_similarity(
                    query_embedding,
                    example.embedding,
                )

            except Exception as exception:

                logger.exception(
                    "Similarity calculation failed: {}",
                    exception,
                )

                continue

            if similarity > highest_similarity:

                highest_similarity = similarity

                best_example = example.text

        # ==========================================
        # Debug Logging
        # ==========================================

        if best_example is not None:

            logger.debug(
                (
                    "Best semantic match "
                    "(similarity={:.3f}): {}"
                ),
                highest_similarity,
                best_example,
            )

        logger.debug(
            "Highest embedding similarity: {:.3f}",
            highest_similarity,
        )

        # ==========================================
        # Threshold
        # ==========================================

        if (
            highest_similarity
            < self.similarity_threshold
        ):
            return 0.0

        issues.append(
            InjectionIssue(
                code="EMBEDDING_SIMILARITY",
                message=(
                    "Prompt is semantically similar "
                    "to known prompt injection examples."
                ),
                score=highest_similarity,
            )
        )

        return highest_similarity
    
    def __repr__(
        self,
    ) -> str:
        """
        Representasi PromptInjectionGuard.
        """

        return (
            f"{self.__class__.__name__}("
            f"threshold={self.threshold}, "
            f"similarity_threshold="
            f"{self.similarity_threshold})"
        )
