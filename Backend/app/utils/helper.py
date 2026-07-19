"""
General Helper Utilities

Berisi fungsi-fungsi bantuan universal untuk manipulasi teks,
masking data sensitif, dan standardisasi format data global.
"""

import re
from decimal import Decimal
from typing import Any, Optional


def clean_spaces(text: str) -> str:
    """
    Membersihkan spasi berlebih, tab, atau baris baru yang berurutan.
    Sangat penting untuk optimasi token LLM (Ollama) dan Guardrails.
    Contoh: "Halo    kuda   " -> "Halo kuda"
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def mask_email(email: str) -> str:
    """
    Menyamarkan email untuk kebutuhan logging keamanan agar data user tidak bocor.
    Contoh: "neuroplanner@gmail.com" -> "ne***********r@gmail.com"
    """
    if not email or "@" not in email:
        return email
    try:
        username, domain = email.split("@", 1)
        if len(username) <= 2:
            return f"{username[0]}*@{domain}"
        return f"{username[0]}{username[1]}{'*' * (len(username) - 3)}{username[-1]}@{domain}"
    except ValueError:
        return email


def format_currency_amount(amount: Any, currency_code: str = "IDR") -> str:
    """
    Memformat tipe Decimal database Trip ke string mata uang yang rapi.
    Contoh: Decimal('1500000.00') -> "Rp 1.500.000,00" atau "USD 1,500.00"
    """
    if amount is None:
        return f"{currency_code} 0"
        
    try:
        val = Decimal(str(amount))
        if currency_code.upper() == "IDR":
            return f"Rp {val:,.2f}".replace(",", ".").replace("Rp ", "Rp ").rstrip(",00")
        return f"{currency_code.upper()} {val:,.2f}"
    except (TypeError, ValueError):
        return f"{currency_code} {amount}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Memotong teks panjang dengan akhiran elipsis (...).
    Berguna untuk preview ringkasan deskripsi itinerary atau log chat.
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].strip() + "..."