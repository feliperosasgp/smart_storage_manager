import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = PROJECT_ROOT / "config.json"
DB_PATH = PROJECT_ROOT / "movements_log.db"

def create_config_interactively():
    print("⚙️ Configuración inicial no encontrada. Vamos a crearla...")

    downloads_dir = input("📥 Ruta de descargas (ej: C:/Users/user/Downloads): ").strip().strip('"')
    buffer_dir = input("📂 Ruta del buffer (ej: D:/Downloads_Buffer): ").strip().strip('"')
    cold_dirs = input("❄️ Cold storage (separadas por coma): ").strip().strip('"').split(",")


    usage_threshold = float(input("📊 Umbral de uso del disco C: (ej: 0.8 para 80%): ") or "0.8")
    move_age_days = int(input("⏳ Edad mínima para mover al buffer (días): ") or "2")
    archive_age_days = int(input("📦 Edad mínima para archivar (días): ") or "30")

    config_data = {
        "downloads_dir": downloads_dir,
        "buffer_dir": buffer_dir,
        "cold_storage_dirs": [x.strip() for x in cold_dirs],
        "usage_threshold": usage_threshold,
        "move_age_days": move_age_days,
        "archive_age_days": archive_age_days,
        "db_path": "movements_log.db"
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    
    print("✅ Configuración guardada exitosamente.")

def load_config():
    if not CONFIG_FILE.exists():
        create_config_interactively()

    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    return {
        "downloads_dir": data["downloads_dir"],
        "buffer_dir": data["buffer_dir"],
        "cold_storage_dirs": data["cold_storage_dirs"],
        "usage_threshold": data.get("usage_threshold", 0.80),
        "move_age_days": data.get("move_age_days", 2),
        "archive_age_days": data.get("archive_age_days", 30),
        "db_path": str(PROJECT_ROOT / data.get("db_path", "movements_log.db"))
    }
