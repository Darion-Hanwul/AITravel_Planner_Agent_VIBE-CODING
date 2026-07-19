"""
Parser Utilities

Utility khusus untuk mengekstrak, membersihkan, dan mengonversi format data,
terutama untuk menangani output mentah (raw output) dari LLM Agent (Ollama).
"""

import json
import re
from typing import Any, Dict, Optional


def extract_json_from_llm(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    Mengekstrak dan mem-parsing JSON dari teks mentah yang dihasilkan oleh LLM.
    Mampu menangani markdown block ```json ... ``` atau teks ekstra di luar JSON.
    
    Returns:
        Optional[Dict[str, Any]]: Objek dictionary jika berhasil, None jika gagal.
    """
    if not raw_text:
        return None

    # Clean space bawaan untuk mempermudah regex
    text = raw_text.strip()

    # 1. Regex untuk mencari pola markdown block ```json ... ``` atau ``` ... ```
    markdown_json_pattern = r"```(?:json)?\s*(\{[\s\S]*?\})\s*```"
    match = re.search(markdown_json_pattern, text)
    
    if match:
        json_content = match.group(1)
    else:
        # 2. Fallback: Cari kurung kurawal pertama '{' hingga terakhir '}' jika tidak dibungkus markdown
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_content = text[start_idx : end_idx + 1]
        else:
            json_content = text

    # 3. Proses parsing ke Python Dictionary
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        # Jika parsing gagal akibat koma menggantung (trailing comma) atau karakter aneh,
        # kita lakukan pembersihan ringan sebelum menyerah
        try:
            # Hapus koma berlebih sebelum kurung tutup: ,} menjadi } dan ,] menjadi ]
            sanitized = re.sub(r",\s*([\]}])", r"\1", json_content)
            return json.loads(sanitized)
        except json.JSONDecodeError:
            return None


def parse_llm_budget_estimation(raw_cost_text: str) -> float:
    """
    Helper untuk mengekstrak angka nominal dari teks rekomendasi biaya LLM.
    Berguna untuk sinkronisasi dengan field Decimal database Anda.
    Contoh: "Sekitar Rp 1.500.000 per hari" -> 1500000.0
    """
    if not raw_cost_text:
        return 0.0
        
    # Ambil hanya deretan angka digital dari teks
    numbers = "".join(re.findall(r"\d+", raw_cost_text))
    try:
        return float(numbers) if numbers else 0.0
    except ValueError:
        return 0.0