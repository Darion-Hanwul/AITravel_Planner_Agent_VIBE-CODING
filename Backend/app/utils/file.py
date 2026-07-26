import os
from pathlib import Path
from fastapi import UploadFile
from app.config.settings import settings

ALLOWED_EXTENSIONS = {
    ".pdf", ".txt", ".docx", ".doc", ".csv", ".xlsx", ".xls", 
    ".md", ".ppt", ".pptx", ".odt", ".rtf"
}


def is_file_allowed(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS and ext != ".json"


def is_file_size_valid(file_size: int) -> bool:
    return file_size <= settings.MAX_UPLOAD_SIZE


def generate_sequenced_filename(filename: str) -> str:
    upload_path = Path(settings.UPLOAD_DIR)
    path_file = Path(filename)
    
    stem = path_file.stem  
    ext = path_file.suffix.lower()  
    
    counter = 1

    new_filename = f"{stem}-Travel-Planner({counter}){ext}"
    
    while (upload_path / new_filename).exists():
        counter += 1
        new_filename = f"{stem}-Travel-Planner({counter}){ext}"
        
    return new_filename


def save_uploaded_file(file: UploadFile) -> str:
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    
    safe_filename = generate_sequenced_filename(file.filename or "unnamed_document")
    file_location = upload_path / safe_filename
    
    with open(file_location, "wb+") as file_object:
        while chunk := file.file.read(1024 * 1024):  
            file_object.write(chunk)
            
    return str(file_location)