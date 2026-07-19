"""
Document Loader

Bertugas membaca berkas fisik dari storage local dan mengekstrak 
seluruh konten teks mentah berdasarkan tipe ekstensi file.
"""

import csv
import docx
from pathlib import Path
import pypdf


class DocumentLoader:
    @staticmethod
    def load_text(file_path: Path) -> str:
        """Membaca berkas teks biasa (.txt atau .md)."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @staticmethod
    def load_pdf(file_path: Path) -> str:
        """Mengekstrak teks dari berkas PDF menggunakan pypdf."""
        text = []
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)

    @staticmethod
    def load_docx(file_path: Path) -> str:
        """Mengekstrak teks dari berkas Word (.docx) menggunakan python-docx."""
        # Memberikan instruksi ignore ke linter agar tidak memicu false-positive error
        doc = docx.Document(file_path)  # type: ignore
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def load_csv(file_path: Path) -> str:
        """Mengubah baris tabel CSV menjadi format teks naratif yang mudah dipahami LLM."""
        text_lines = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            for row in reader:
                if headers:
                    # Contoh format: "Kolom1: nilai1, Kolom2: nilai2"
                    items = [f"{headers[i]}: {row[i]}" for i in range(min(len(headers), len(row)))]
                    text_lines.append(", ".join(items))
                else:
                    text_lines.append(" ".join(row))
        return "\n".join(text_lines)

    def load_file(self, file_path_str: str) -> str:
        """
        Fungsi gerbang utama (orchestrator) untuk memuat dokumen secara dinamis 
        berdasarkan jenis ekstensi berkas.
        """
        file_path = Path(file_path_str)
        if not file_path.exists():
            raise FileNotFoundError(f"Berkas tidak ditemukan di path: {file_path_str}")

        ext = file_path.suffix.lower()

        if ext in [".txt", ".md"]:
            return self.load_text(file_path)
        elif ext == ".pdf":
            return self.load_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return self.load_docx(file_path)
        elif ext in [".csv", ".xlsx", ".xls"]:
            return self.load_csv(file_path)
        else:
            return self.load_text(file_path)