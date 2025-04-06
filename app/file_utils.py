import os
import hashlib
from pathlib import Path
from datetime import datetime

EXTENSION_GROUPS = {
    "Documentos": [".doc", ".docx", ".pdf", ".txt", ".md", ".odt"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Hojas_de_calculo": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentaciones": [".ppt", ".pptx", ".odp"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac"],
}

def get_category(file: Path) -> str:
    """Determina la categoría del archivo según su extensión"""
    ext = file.suffix.lower()
    for category, extensions in EXTENSION_GROUPS.items():
        if ext in extensions:
            return category
    return f"Otros{ext}"

def get_file_age_days(file: Path):
    """Calcula cuántos días han pasado desde la última modificación del archivo"""
    modified_time = file.stat().st_mtime
    return (datetime.now() - datetime.fromtimestamp(modified_time)).days

def hash_file(file: Path):
    """Genera hash SHA256 del archivo para detectar duplicados"""
    h = hashlib.sha256()
    with open(file, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
