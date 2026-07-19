"""
Text Splitter Utilities

Bertugas memotong dokumen teks panjang menjadi potongan kecil (chunks)
secara cerdas berdasarkan separator alami, dengan mematuhi batasan
CHUNK_SIZE dan CHUNK_OVERLAP dari konfigurasi global.
"""

from typing import List, Optional
from app.config.settings import settings


class TextSplitter:
    def __init__(self, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None) -> None:
        # Menggunakan nilai dari settings.py sebagai fallback jika tidak diisi manual
        self.chunk_size: int = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap: int = chunk_overlap or settings.CHUNK_OVERLAP
        
        # Karakter pemisah berdasarkan prioritas kedekatan konteks bahasa
        self.separators: List[str] = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        """
        Memotong string teks tunggal menjadi list chunks menggunakan metode rekursif 
        agar potongan kalimat tetap natural dan tidak terputus secara acak.
        """
        if not text or not text.strip():
            return []

        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        """
        Inti algoritma pemotong teks rekursif.
        """
        # Jika teks sudah lebih kecil dari chunk_size, tidak perlu dipotong lagi
        if len(text) <= self.chunk_size:
            return [text]

        # Pilih separator teratas yang tersedia
        separator = separators[0]
        next_separators = separators[1:]

        # Pecah teks berdasarkan separator yang dipilih
        if separator == "":
            splits = list(text)
        else:
            splits = text.split(separator)

        chunks: List[str] = []
        current_chunk: List[str] = []
        current_length = 0

        for split in splits:
            # Hitung estimasi panjang jika split digabungkan dengan current_chunk
            split_len = len(split)
            # Ditambah panjang separator jika current_chunk tidak kosong
            addition = len(separator) if current_chunk else 0

            if current_length + split_len + addition <= self.chunk_size:
                current_chunk.append(split)
                current_length += split_len + addition
            else:
                # Jika current_chunk sudah penuh, gabungkan dan simpan
                if current_chunk:
                    joined_text = separator.join(current_chunk)
                    chunks.append(joined_text)
                
                # Jika potongan split tunggal itu sendiri melebihi chunk_size,
                # oper ke separator berikutnya yang lebih kecil (rekursif)
                if split_len > self.chunk_size and next_separators:
                    chunks.extend(self._recursive_split(split, next_separators))
                    current_chunk = []
                    current_length = 0
                else:
                    # Buat chunk baru dimulai dari pecahan saat ini dan hapus typo range_len
                    current_chunk = [split]
                    current_length = split_len

        # Jangan lupa simpan sisa pecahan terakhir jika ada
        if current_chunk:
            chunks.append(separator.join(current_chunk))

        # Terapkan strategi overlap (irisan teks) antar chunk berdekatan
        return self._handle_overlap(chunks)

    def _handle_overlap(self, chunks: List[str]) -> List[str]:
        """
        Menambahkan potongan teks overlap di awal setiap chunk berikutnya
        agar konteks data tidak hilang di antara batas pemotongan.
        """
        if len(chunks) <= 1 or self.chunk_overlap <= 0:
            return chunks

        overlapped_chunks: List[str] = [chunks[0]]

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i - 1]
            current_chunk = chunks[i]

            # Ambil potongan karakter terakhir dari chunk sebelumnya sebesar chunk_overlap
            overlap_prefix = prev_chunk[-self.chunk_overlap:]
            
            # Gabungkan di depan chunk saat ini
            new_chunk = overlap_prefix + current_chunk
            overlapped_chunks.append(new_chunk)

        return overlapped_chunks