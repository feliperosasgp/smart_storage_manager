import argparse
import sqlite3
from pathlib import Path
from tabulate import tabulate

from config import load_config
from file_utils import get_file_age_days, hash_file, get_category
from database import init_db, file_already_moved, log_file_movement
import psutil
import shutil

config = load_config()
DOWNLOADS_DIR = Path(config["downloads_dir"])
BUFFER_DIR = Path(config["buffer_dir"])
COLD_STORAGE_DIRS = [Path(p) for p in config["cold_storage_dirs"]]
USAGE_THRESHOLD = config["usage_threshold"]
MOVE_AGE_DAYS = config["move_age_days"]
ARCHIVE_AGE_DAYS = config["archive_age_days"]
DB_PATH = config["db_path"]

def get_disk_usage(path: Path):
    return psutil.disk_usage(str(path))

def move_to_buffer(force=False):
    print("📥 Buscando archivos para mover al buffer...")
    usage = get_disk_usage(DOWNLOADS_DIR)
    if force or usage.percent / 100 >= USAGE_THRESHOLD:
        for file in DOWNLOADS_DIR.iterdir():
            if file.is_file() and get_file_age_days(file) >= MOVE_AGE_DAYS:
                file_hash = hash_file(file)
                if not file_already_moved(file_hash):
                    category = get_category(file)
                    dest_dir = BUFFER_DIR / category
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    dest = dest_dir / file.name
                    shutil.move(str(file), str(dest))
                    log_file_movement(file.name, str(file), str(dest), file_hash)
                    print(f"✅ Movido al buffer: {file.name} ({category})")
                else:
                    print(f"🔁 {file.name} ya había sido movido.")
    else:
        print("✅ El disco aún no supera el umbral, no se requiere mover.")

def archive_old_files():
    print("📦 Buscando archivos antiguos para archivar en cold storage...")
    for file in BUFFER_DIR.rglob("*"):
        if file.is_file() and get_file_age_days(file) >= ARCHIVE_AGE_DAYS:
            file_hash = hash_file(file)
            if not file_already_moved(file_hash):
                category = get_category(file)
                cold_target = min(COLD_STORAGE_DIRS, key=lambda d: get_disk_usage(d).percent)
                dest_dir = cold_target / category
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / file.name
                shutil.move(str(file), str(dest))
                log_file_movement(file.name, str(file), str(dest), file_hash)
                print(f"❄️ Archivado en {cold_target}: {file.name} ({category})")
            else:
                print(f"🔁 {file.name} ya había sido archivado.")

def list_recent_movements(limit=10):
    if not Path(DB_PATH).exists():
        print("⚠️ No hay registros aún.")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, original_path, new_path, moved_at FROM file_movements ORDER BY moved_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    print(tabulate(rows, headers=["Archivo", "Origen", "Destino", "Fecha"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    init_db()

    parser = argparse.ArgumentParser(description="📦 Smart Storage CLI")
    parser.add_argument("--move-buffer", action="store_true", help="Mover archivos del disco principal al buffer")
    parser.add_argument("--archive", action="store_true", help="Mover archivos del buffer al cold storage")
    parser.add_argument("--all", action="store_true", help="Ejecutar ambos flujos (forzado)")
    parser.add_argument("--list", action="store_true", help="Mostrar los últimos archivos movidos")
    args = parser.parse_args()

    if args.move_buffer:
        move_to_buffer()
    elif args.archive:
        archive_old_files()
    elif args.all:
        move_to_buffer(force=True)
        archive_old_files()
    elif args.list:
        list_recent_movements()
    else:
        parser.print_help()
