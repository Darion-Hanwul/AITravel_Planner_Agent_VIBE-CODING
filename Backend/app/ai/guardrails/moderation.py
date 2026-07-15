"""
Content Moderation Guard untuk TravelPlannerAgent.

Moderation Guard bertanggung jawab mendeteksi
konten yang berisiko sebelum diproses oleh AI.

Responsibility
--------------

- Hate Speech Detection
- Harassment Detection
- Violence Detection
- Self Harm Detection
- Sexual Content Detection
- Illegal Activity Detection
- Fraud Detection
- Privacy Detection
- Cyber Abuse Detection
- Travel Safety Detection
- Rule-Based Risk Scoring

Tidak bertanggung jawab terhadap

- Input Validation
- Prompt Injection Detection
- Tool Calling
- RAG
- LangGraph
- LLM
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re

from app.config.settings import settings
from app.core.logger import logger


class SeverityLevel(str, Enum):
    """Tingkat keparahan hasil moderation."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskCategory(str, Enum):
    """Kategori risiko yang dideteksi oleh Moderation Guard."""
    HATE = "HATE"
    HARASSMENT = "HARASSMENT"
    VIOLENCE = "VIOLENCE"
    SELF_HARM = "SELF_HARM"
    SEXUAL = "SEXUAL"
    ILLEGAL = "ILLEGAL"
    FRAUD = "FRAUD"
    PRIVACY = "PRIVACY"
    CYBER = "CYBER"
    TRAVEL_SAFETY = "TRAVEL_SAFETY"


@dataclass(slots=True)
class ModerationIssue:
    """Merepresentasikan satu hasil deteksi moderation."""
    category: RiskCategory
    code: str
    message: str
    score: float


@dataclass(slots=True)
class ModerationResult:
    """Hasil pemeriksaan moderation."""
    allowed: bool
    score: float
    severity: SeverityLevel
    issues: list[ModerationIssue] = field(default_factory=list)


class ModerationGuard:
    """
    Rule-Based Content Moderation.
    Guard ini dijalankan setelah PromptInjectionGuard.
    """

    def __init__(self) -> None:
        """Inisialisasi Moderation Guard."""
        logger.info("Initializing ModerationGuard.")

        # =====================================
        # Threshold & Weights
        # =====================================
        self.threshold = settings.MODERATION_THRESHOLD
        self.low_threshold = settings.MODERATION_LOW_THRESHOLD
        self.medium_threshold = settings.MODERATION_MEDIUM_THRESHOLD
        self.high_threshold = settings.MODERATION_HIGH_THRESHOLD
        self.critical_threshold = settings.MODERATION_CRITICAL_THRESHOLD

        self.regex_weight = settings.MODERATION_REGEX_WEIGHT
        self.keyword_weight = settings.MODERATION_KEYWORD_WEIGHT
        self.regex_early_stop = settings.MODERATION_REGEX_EARLY_STOP
        self.combined_early_stop = settings.MODERATION_COMBINED_EARLY_STOP

        # =====================================
        # Detection Rules Initialization
        # =====================================
        self.regex_patterns = self._load_regex_patterns()
        self.keyword_groups = self._load_keyword_groups()
        self.keyword_patterns = self._compile_keyword_patterns()

        logger.info("ModerationGuard initialized successfully.")

    # =====================================
    # Public API
    # =====================================
    def check(self, prompt: str) -> ModerationResult:
        
        """Memeriksa prompt pengguna terhadap seluruh kategori risiko keamanan."""

        if not prompt or not prompt.strip():
            return ModerationResult(allowed=True, score=0.0, severity=SeverityLevel.LOW)

        logger.info("Executing content moderation check.")
        
        # 1. Jalankan Regex Detection Engine
        regex_issues = self._run_regex_detection(prompt)
        
        # Early stop check
        regex_score = sum(issue.score for issue in regex_issues)
        if regex_score >= self.regex_early_stop:
            logger.warning(f"Moderation regex early stop triggered. Score: {regex_score}")
            severity = self._determine_severity(regex_score)
            return ModerationResult(allowed=False, score=regex_score, severity=severity, issues=regex_issues)

        # 2. Jalankan Keyword Detection Engine
        keyword_issues = self._run_keyword_detection(prompt)
        
        # Gabungkan issues & hitung weighted score
        all_issues = regex_issues + keyword_issues
        total_score = self._calculate_weighted_score(regex_issues, keyword_issues)
        severity = self._determine_severity(total_score)
        
        allowed = total_score < self.threshold
        logger.info(f"Moderation check completed. Allowed: {allowed}, Total Score: {total_score}, Severity: {severity}")
        
        return ModerationResult(
            allowed=allowed,
            score=total_score,
            severity=severity,
            issues=all_issues
        )

    # =====================================
    # Internal Helper Methods
    # =====================================
    def _determine_severity(self, score: float) -> SeverityLevel:
        """Menentukan tingkat keparahan berdasarkan total risk score."""
        if score >= self.critical_threshold:
            return SeverityLevel.CRITICAL
        if score >= self.high_threshold:
            return SeverityLevel.HIGH
        if score >= self.medium_threshold:
            return SeverityLevel.MEDIUM
        return SeverityLevel.LOW

    def _calculate_weighted_score(self, regex_issues: list[ModerationIssue], keyword_issues: list[ModerationIssue]) -> float:
        """Menghitung total nilai risiko menggunakan Weighted Scoring Pattern."""
        raw_regex_score = sum(issue.score for issue in regex_issues)
        raw_keyword_score = sum(issue.score for issue in keyword_issues)

        normalized_regex = min(raw_regex_score, 1.0)
        normalized_keyword = min(raw_keyword_score, 1.0)

        weighted_score = (normalized_regex * self.regex_weight) + (normalized_keyword * self.keyword_weight)
        return round(float(min(weighted_score, 1.0)), 4)

    # =====================================
    # Rules Loading & Compilation
    # =====================================
    def _load_regex_patterns(self) -> dict[RiskCategory, list[re.Pattern[str]]]:
        """Memuat dan mengompilasi pola regex untuk 10 kategori risiko."""
        raw_patterns: dict[RiskCategory, list[str]] = {
            RiskCategory.HATE: [
                r"(bunuh|musnahkan|hancurkan)\s+(ras|suku|agama|kaum)\s+\w+",
                r"pribumi\s+(vs|lawan)\s+(cina|tionghoa|pendatang)",
                r"dasar\s+(kafir|goyim|antek|babi|anjing)\s+\w+"
            ],
            RiskCategory.HARASSMENT: [
                r"(kamu|lu)\s+(bodoh|tolol|goblok|pecundang|cacat|miskin)\s+banget",
                r"saya\s+(akan|mau)\s+(neror|teror|nguntit|stalking)\s+\w+",
                r"sebar\s+(foto|video|aib|data)\s+si\s+\w+"
            ],
            RiskCategory.VIOLENCE: [
                r"(rakit|membuat|cara\s+bikin)\s+(bom|molotov|senjata\s+api|peledak)",
                r"(tembak|tusuk|gorok|pancung|bantai)\s+(saja|si|orang)",
                r"serang\s+(kantor|polisi|gedung|fasilitas\s+umum)"
            ],
            RiskCategory.SELF_HARM: [
                r"(cara|tips|panduan)\s+(bunuh\s+diri|sayat\s+nangan|potong\s+nadi)",
                r"(gantung|lompat|terjun|tenggelam)\s+diri",
                r"minum\s+(racun|sianida|overdosis|obat\s+serangga)"
            ],
            RiskCategory.SEXUAL: [
                r"(video|foto|konten|link)\s+(porn[oo]|bokep|lendir|pemerkosaan)",
                r"(jual|sewa|tarif)\s+(bo|psk|pelacur|lendir)",
                r"pemerkosaan\s+massal|inses|pedofil"
            ],
            RiskCategory.ILLEGAL: [
                r"(beli|jual|transaksi|edar)\s+(ganja|sabu|ekstasi|putau|narkoba)",
                r"(situs|link|aplikasi)\s+(judi\s+online|slot|gacor|zeus)",
                r"(unduh|download|bajakan|crack)\s+(software|film|aplikasi)"
            ],
            RiskCategory.FRAUD: [
                r"(buat|cetak|jual)\s+(ktp|paspor|ijazah|uang)\s+palsu",
                r"(bobol|hack|phishing|carding)\s+(rekening|atm|kartu\s+kredit|akun)",
                r"investasi\s+(pasti|untung\s+besar|cepat)\s+(bodong|ponzi)"
            ],
            RiskCategory.PRIVACY: [
                r"(nomor|no)\s+(hp|wa|telp)\s+\d{10,13}",
                r"nik\s+\d{16}|no\s+rekening\s+\d{8,15}",
                r"(alamat|rumah|lokasi)\s+pribadi\s+si\s+\w+"
            ],
            RiskCategory.CYBER: [
                r"(dodos|ddos|botnet|brute\s+force)\s+(server|website|api)",
                r"(injeksi|inject)\s+(sql|payload|xss)\s+(ke|pada)",
                r"(sebar|kirim)\s+(malware|ransomware|trojan|virus)"
            ],
            RiskCategory.TRAVEL_SAFETY: [
                r"(rute|cara)\s+(masuk|menyusup)\s+ke\s+(daerah\s+konflik|zona\s+perang)",
                r"selundupkan\s+(barang|alkohol|senjata)\s+lewat\s+imigrasi",
                r"hindari\s+(pemeriksaan|petugas|pajak|bea\s+cukai)\s+bandara"
            ]
        }

        compiled_patterns: dict[RiskCategory, list[re.Pattern[str]]] = {}
        for category, str_list in raw_patterns.items():
            compiled_patterns[category] = [re.compile(p, re.IGNORECASE) for p in str_list]
        return compiled_patterns

    def _load_keyword_groups(self) -> dict[RiskCategory, list[str]]:
        """Memuat kamus besar kata kunci berisiko tinggi untuk 10 kategori risiko."""
        return {
            RiskCategory.HATE: [
                "anjing", "babi", "lonte", "kafir", "goyim", "nigga", "bencong", 
                "autis", "cacat", "pribumi", "antek", "zionis", "komunis"
            ],
            RiskCategory.HARASSMENT: [
                "tolol", "goblok", "bego", "bodoh", "pecundang", "cupu", "jelek",
                "teror", "ancam", "stalking", "intimidasi", "doxing", "bully"
            ],
            RiskCategory.VIOLENCE: [
                "bom", "molotov", "peledak", "teroris", "senjata", "pisau", "gorok",
                "tembak", "bantai", "mutilasi", "eksekusi", "darah", "pembunuhan"
            ],
            RiskCategory.SELF_HARM: [
                "bunuh diri", "suicide", "sayat nadi", "gantung diri", "sianida",
                "racun rumput", "overdosis", "lompat gedung", "menenggelamkan diri"
            ],
            RiskCategory.SEXUAL: [
                "porno", "pornography", "bokep", "lendir", "bo", "open bo", "psk",
                "pelacur", "pemerkosaan", "ngentot", "kontol", "memek", "hentai"
            ],
            RiskCategory.ILLEGAL: [
                "narkoba", "sabu", "ganja", "ekstasi", "judi", "slot", "gacor",
                "slot88", "bajakan", "torrent", "smuggling", "penyelundupan"
            ],
            RiskCategory.FRAUD: [
                "scam", "phishing", "carding", "ponzi", "bodong", "palsu", "pemalsuan",
                "ijazah palsu", "uang palsu", "manipulasi", "penggelapan", "korupsi"
            ],
            RiskCategory.PRIVACY: [
                "nik", "ktp", "paspor", "passport", "rekening", "cc", "credit card",
                "cvv", "atm", "password", "pin", "api key", "secret token"
            ],
            RiskCategory.CYBER: [
                "ddos", "malware", "ransomware", "trojan", "exploit", "backdoor",
                "brute force", "deface", "hack", "cracking", "keylogger", "payload"
            ],
            RiskCategory.TRAVEL_SAFETY: [
                "zona perang", "daerah konflik", "jalur tikus", "suap imigrasi",
                "visa palsu", "black market", "kartel", "terorisme travel", "ilegal border"
            ]
        }

    def _compile_keyword_patterns(self) -> dict[RiskCategory, re.Pattern[str] | None]:
        """Mengompilasi kelompok kata kunci menjadi regex tunggal untuk pencarian cepat."""
        compiled: dict[RiskCategory, re.Pattern[str] | None] = {}
        for category, keywords in self.keyword_groups.items():
            if not keywords:
                compiled[category] = None
                continue
            escaped_keywords = [re.escape(kw) for kw in keywords]
            pattern_str = r"\b(" + "|".join(escaped_keywords) + r")\b"
            compiled[category] = re.compile(pattern_str, re.IGNORECASE)
        return compiled

    # =====================================
    # Detection Execution Engines
    # =====================================
    def _run_regex_detection(self, prompt: str) -> list[ModerationIssue]:
        """Mengeksekusi pemindaian regular expression dengan penalti skor terkalibrasi."""
        issues: list[ModerationIssue] = []
        category_weights: dict[RiskCategory, float] = {
            RiskCategory.HATE: 0.50,
            RiskCategory.HARASSMENT: 0.40,
            RiskCategory.VIOLENCE: 0.85,
            RiskCategory.SELF_HARM: 0.90,
            RiskCategory.SEXUAL: 0.70,
            RiskCategory.ILLEGAL: 0.60,
            RiskCategory.FRAUD: 0.65,
            RiskCategory.PRIVACY: 0.55,
            RiskCategory.CYBER: 0.75,
            RiskCategory.TRAVEL_SAFETY: 0.70
        }

        for category, patterns in self.regex_patterns.items():
            base_score = category_weights.get(category, 0.40)
            for pattern in patterns:
                match = pattern.search(prompt)
                if match:
                    matched_text = match.group(0)
                    issues.append(
                        ModerationIssue(
                            category=category,
                            code=f"REG_{category.value}_{len(issues) + 1:03d}",
                            message=f"Kritikal: Pola berisiko terdeteksi lewat regex: '{matched_text[:40]}...'",
                            score=base_score
                        )
                    )
        return issues

    def _run_keyword_detection(self, prompt: str) -> list[ModerationIssue]:
        """Mengeksekusi pemindaian kata kunci terkompilasi dengan akumulasi skor logaritmik."""
        issues: list[ModerationIssue] = []
        keyword_base_scores: dict[RiskCategory, float] = {
            RiskCategory.HATE: 0.20,
            RiskCategory.HARASSMENT: 0.15,
            RiskCategory.VIOLENCE: 0.35,
            RiskCategory.SELF_HARM: 0.40,
            RiskCategory.SEXUAL: 0.30,
            RiskCategory.ILLEGAL: 0.25,
            RiskCategory.FRAUD: 0.30,
            RiskCategory.PRIVACY: 0.20,
            RiskCategory.CYBER: 0.35,
            RiskCategory.TRAVEL_SAFETY: 0.30
        }

        for category, pattern in self.keyword_patterns.items():
            if not pattern:
                continue
                
            matches = pattern.findall(prompt)
            if matches:
                unique_matches = sorted(list(set(matches)))
                base_kw_score = keyword_base_scores.get(category, 0.15)
                calculated_score = min(len(unique_matches) * base_kw_score, 1.0)
                
                issues.append(
                    ModerationIssue(
                        category=category,
                        code=f"KEY_{category.value}_001",
                        message=f"Terdeteksi kata kunci terlarang ({len(unique_matches)} ditemukan): {', '.join(unique_matches[:5])}",
                        score=round(calculated_score, 3)
                    )
                )
        return issues

    # =====================================
    # Utilities
    # =====================================
    def __repr__(self) -> str:
        """Representasi string resmi untuk objek ModerationGuard."""
        return (
            f"ModerationGuard("
            f"threshold={self.threshold}, "
            f"regex_weight={self.regex_weight}, "
            f"keyword_weight={self.keyword_weight})"
        )