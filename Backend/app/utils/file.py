"""
File Utilities

Utility terstandarisasi untuk menangani manajemen file upload (RAG Documents),
validasi ukuran berkas, penyaringan ekstensi aman, dan penamaan berkas berurutan.
"""

import os
from pathlib import Path
from fastapi import UploadFile
from app.config.settings import settings

# Mengunci semua jenis dokumen umum sesuai permintaan (Kecuali .json)
ALLOWED_EXTENSIONS = {
    ".pdf", ".txt", ".docx", ".doc", ".csv", ".xlsx", ".xls", 
    ".md", ".ppt", ".pptx", ".odt", ".rtf"
}


def is_file_allowed(filename: str) -> bool:
    """
    Memeriksa apakah ekstensi berkas diperbolehkan oleh sistem RAG (Semua kecuali .json).
    """
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS and ext != ".json"


def is_file_size_valid(file_size: int) -> bool:
    """
    Memvalidasi apakah ukuran berkas tidak melebihi batas MAX_UPLOAD_SIZE.
    """
    return file_size <= settings.MAX_UPLOAD_SIZE


def generate_sequenced_filename(filename: str) -> str:
    """
    Membuat nama berkas unik berurutan jika terjadi konflik nama di server.
    Contoh: "saya.pdf" -> "saya-Travel-Planner(1).pdf" -> "saya-Travel-Planner(2).pdf"
    """
    upload_path = Path(settings.UPLOAD_DIR)
    path_file = Path(filename)
    
    stem = path_file.stem  # Nama file tanpa ekstensi (cth: "saya")
    ext = path_file.suffix.lower()  # Ekstensi file (cth: ".pdf")
    
    counter = 1
    # Format penamaan awal sesuai permintaan Anda
    new_filename = f"{stem}-Travel-Planner({counter}){ext}"
    
    # Lakukan loop untuk mencari angka yang belum digunakan di folder storage
    while (upload_path / new_filename).exists():
        counter += 1
        new_filename = f"{stem}-Travel-Planner({counter}){ext}"
        
    return new_filename


def save_uploaded_file(file: UploadFile) -> str:
    """
    Menyimpan berkas yang diunggah secara aman dengan nama terurut,
    lalu mengembalikan string lokasi path file yang disimpan.
    """
    # Pastikan folder target UPLOAD_DIR sudah dibuat
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    # Tentukan nama file final yang aman & berurutan
    safe_filename = generate_sequenced_filename(file.filename or "unnamed_document")
    file_location = upload_path / safe_filename
    
    # Proses streaming chunk data ke storage agar hemat RAM
    with open(file_location, "wb+") as file_object:
        while chunk := file.file.read(1024 * 1024):  # Baca per 1 MB
            file_object.write(chunk)
            
    return str(file_location)