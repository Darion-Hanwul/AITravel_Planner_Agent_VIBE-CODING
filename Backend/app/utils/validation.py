"""
Validation Utilities (Guardrails)

Utility terstandarisasi untuk menegakkan aturan keamanan input teks (Guardrails)
sebelum diproses oleh LLM Agent (Ollama), sesuai parameter di config setting.
"""

import re
from typing import Tuple
from app.config.settings import settings


def validate_llm_prompt(prompt: str) -> Tuple[bool, str]:
    """
    Validasi keamanan teks prompt berdasarkan parameter Guardrails di setting.py.
    
    Returns:
        Tuple[bool, str]: (True/False status validasi, Pesan keterangan jika gagal/sukses)
    """
    if not prompt or not prompt.strip():
        return False, "Prompt tidak boleh kosong."

    # 1. Validasi Panjang Karakter (Length Check)
    prompt_len = len(prompt)
    if prompt_len < settings.MIN_PROMPT_LENGTH:
        return False, f"Prompt terlalu pendek. Minimal {settings.MIN_PROMPT_LENGTH} karakter."
    
    if prompt_len > settings.MAX_PROMPT_LENGTH:
        return False, f"Prompt terlalu panjang. Maksimal {settings.MAX_PROMPT_LENGTH} karakter."

    # 2. Validasi Spasi Berurutan Ekstrim (Consecutive Whitespace Check)
    # Mencari spasi/tab/enter berulang yang melebihi batas
    whitespace_pattern = rf"\s{{{settings.MAX_CONSECUTIVE_WHITESPACE + 1},}}"
    if re.search(whitespace_pattern, prompt):
        return False, "Prompt mengandung spasi atau baris baru berlebih yang mencurigakan."

    # 3. Validasi Karakter Berulang Ekstrim (Repeated Characters Check)
    # Contoh: "aaaaa..." yang bisa merusak konsentrasi LLM attention mechanism
    repeated_char_pattern = rf"(.)\1{{{settings.MAX_REPEATED_CHARACTERS},}}"
    if re.search(repeated_char_pattern, prompt):
        return False, "Prompt mengandung pengulangan karakter yang tidak wajar."

    # 4. Validasi Jumlah Emoji (Emoji Spam Check)
    # Menghitung karakter emoji yang dikirim dalam satu prompt
    emoji_count = len(re.findall(r"[\U00010000-\U0010ffff]", prompt))
    if emoji_count > settings.MAX_EMOJI_COUNT:
        return False, f"Prompt mengandung terlalu banyak emoji (Maksimal {settings.MAX_EMOJI_COUNT})."

    return True, "Prompt aman dan memenuhi standar guardrails."