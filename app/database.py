import sqlite3
from config import load_config

config = load_config()
DB_PATH = config["db_path"]

def init_db():
    """Crea la base de datos para registrar movimientos si no existe"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS file_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            original_path TEXT,
            new_path TEXT,
            hash TEXT,
            moved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def file_already_moved(file_hash: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM file_movements WHERE hash = ?", (file_hash,))
    result = c.fetchone()
    conn.close()
    return result is not None

def log_file_movement(filename, original_path, new_path, file_hash):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO file_movements (filename, original_path, new_path, hash)
        VALUES (?, ?, ?, ?)
    ''', (filename, original_path, new_path, file_hash))
    conn.commit()
    conn.close()
