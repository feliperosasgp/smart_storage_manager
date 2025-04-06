import shutil
import psutil
import argparse
from pathlib import Path
from config import load_config
from file_utils import get_file_age_days, hash_file, get_category
from database import init_db, file_already_moved, log_file_movement

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
    usage = get_disk_usage(DOWNLOADS_DIR)
    if force or usage.percent / 100 >= USAGE_THRESHOLD:
        print(f"➡️ Ejecutando movimiento al buffer...")
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
                    print(f"✅ {file.name} movido al buffer ({category})")
                else:
                    print(f"🔁 {file.name} ya movido (hash duplicado)")

def archive_old_files():
    print(f"❄️ Archivando archivos viejos del buffer...")
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
                print(f"📦 {file.name} archivado en {cold_target} ({category})")

if __name__ == "__main__":
    init_db()

    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--buffer', action='store_true')
    parser.add_argument('--archive', action='store_true')
    args = parser.parse_args()

    if args.force:
        move_to_buffer(force=True)
        archive_old_files()
    elif args.buffer:
        move_to_buffer()
    elif args.archive:
        archive_old_files()
    else:
        print("⚠️ Usa --force, --buffer o --archive para ejecutar el flujo deseado.")
