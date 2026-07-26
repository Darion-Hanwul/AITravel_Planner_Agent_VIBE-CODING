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
    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"

    CRITICAL = "CRITICAL"


@dataclass(slots=True)
class InjectionIssue:

    code: str

    message: str

    score: float


@dataclass(slots=True)
class InjectionResult:
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
    text: str

    embedding: list[float]

class PromptInjectionGuard:
    def __init__(
        self,
    ) -> None:
        """
        Inisialisasi Prompt Injection Guard.
        """

        logger.info(
            "Initializing PromptInjectionGuard."
        )

        self.embedding_service = (
            EmbeddingService()
        )

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

        self.regex_weight = (
            settings.PROMPT_INJECTION_REGEX_WEIGHT
        )

        self.keyword_weight = (
            settings.PROMPT_INJECTION_KEYWORD_WEIGHT
        )

        self.embedding_weight = (
            settings.PROMPT_INJECTION_EMBEDDING_WEIGHT
        )

        self.examples_path = Path(
            settings.PROMPT_INJECTION_EXAMPLES_FILE,
        )

        self.prompt_examples = (
            self._load_prompt_examples()
        )

        self.example_embeddings = (
            self._build_example_embeddings()
        )

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

    def _load_prompt_examples(
        self,
    ) -> list[str]:
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
        return {

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

        "TOOLS_DISCLOSURE": (
            re.compile(
                r"(show|reveal|display|list|print)\s+.*"
                r"(internal\s+tool|tool\s+schema|tool\s+list|available\s+tools)",
                re.IGNORECASE,
            ),
            0.40,
        ),

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
        return {

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

            "ROLE": (
                [
                    "act as",
                    "pretend",
                    "roleplay",
                    "simulate",
                ],
                0.25,
            ),

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

    def check(
        self,
        prompt: str,
    ) -> InjectionResult:
        logger.debug(
            "Starting prompt injection detection."
        )

        issues: list[InjectionIssue] = []

        matched_patterns: list[str] = []

        regex_score = self._regex_detection(
            prompt=prompt,
            issues=issues,
            matched_patterns=matched_patterns,
        )

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
        return self.check(
            prompt,
        ).allowed
    
    def risk_score(
        self,
        prompt: str,
    ) -> float:
        return self.check(
            prompt,
        ).score

    def risk_level(
        self,
        prompt: str,
    ) -> RiskLevel:
        return self.check(
            prompt,
        ).risk_level

    def _calculate_score(
        self,
        *,
        regex_score: float,
        keyword_score: float,
        embedding_score: float,
    ) -> float:
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

    def _regex_detection(
        self,
        *,
        prompt: str,
        issues: list[InjectionIssue],
        matched_patterns: list[str],
    ) -> float:
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

        return (
            f"{self.__class__.__name__}("
            f"threshold={self.threshold}, "
            f"similarity_threshold="
            f"{self.similarity_threshold})"
        )
