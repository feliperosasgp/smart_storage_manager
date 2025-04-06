import streamlit as st
import json
from pathlib import Path
from config import CONFIG_FILE, DB_PATH
import sqlite3
import pandas as pd
import subprocess
import os

CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_config():
    if not Path(CONFIG_FILE).exists():
        return None
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

st.set_page_config(page_title="Smart Storage", layout="wide")
st.title("⚙️ Configuración del sistema de almacenamiento")

# Sección de configuración de rutas
downloads_dir = st.text_input("📥 Ruta de descargas", value="C:/Users/user/Downloads")
buffer_dir = st.text_input("📂 Ruta del buffer", value="D:/Downloads_Buffer")
cold_dirs = st.text_input("❄️ Cold storage (separados por coma)", value="E:/ColdStorage1,F:/ColdStorage2")

# Parámetros adicionales
usage_threshold = st.slider("📊 Umbral de uso del disco C:", 0.5, 0.95, 0.80)
move_age_days = st.number_input("⏳ Edad mínima para mover al buffer (días)", min_value=1, value=2)
archive_age_days = st.number_input("📦 Edad mínima para archivar en cold storage (días)", min_value=1, value=30)

if st.button("💾 Guardar configuración"):
    cold_storage_dirs = [x.strip() for x in cold_dirs.split(",")]
    config_data = {
        "downloads_dir": downloads_dir,
        "buffer_dir": buffer_dir,
        "cold_storage_dirs": cold_storage_dirs,
        "usage_threshold": usage_threshold,
        "move_age_days": move_age_days,
        "archive_age_days": archive_age_days,
        "db_path": "movements_log.db"
    }
    save_config(config_data)
    st.success("✅ Configuración guardada")

# --- BOTONES DE ACCIÓN ---
st.markdown("---")
st.subheader("⚙️ Acciones disponibles")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Mover todo ahora (ignorar umbral)"):
        os.system("python main.py --force")
        st.success("✅ Movimiento completo ejecutado")

with col2:
    if st.button("📂 Mover al buffer (normal)"):
        os.system("python main.py --buffer")
        st.success("✅ Archivos movidos al buffer")

with col3:
    if st.button("❄️ Archivar a cold storage"):
        os.system("python main.py --archive")
        st.success("✅ Archivos archivados")

# --- HISTORIAL DE MOVIMIENTOS ---
st.markdown("---")
st.subheader("📦 Historial de movimientos")

if Path(DB_PATH).exists():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM file_movements ORDER BY moved_at DESC", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ Aún no se ha generado el historial.")
