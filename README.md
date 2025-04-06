📄 README.md para smart_storage_manager
markdown
Copiar
Editar
# 📦 Smart Storage Manager

Gestor inteligente de almacenamiento para estaciones de trabajo con múltiples discos.  
Automatiza el movimiento de archivos entre discos según antigüedad, tipo y espacio disponible.  
Ideal para liberar tu disco principal sin perder trazabilidad.

---

## 🚀 Características principales

✅ Mueve archivos automáticamente desde la carpeta de descargas al buffer (disco secundario)  
✅ Archiva archivos antiguos desde el buffer a almacenamiento frío (discos extendidos)  
✅ Clasifica por tipo de archivo (documentos, imágenes, vídeos, etc.)  
✅ Historial de movimientos con SQLite  
✅ Interfaz visual con Streamlit y también versión CLI para programar tareas  
✅ Configurable y portable

---

## 📂 Estructura

smart_storage_manager/ ├── app/ │ ├── cli.py # Modo consola │ ├── dashboard.py # Interfaz visual (Streamlit) │ ├── main.py # Lógica completa de ejecución │ ├── config.py # Carga y guarda configuración │ ├── file_utils.py # Herramientas para clasificar archivos │ └── database.py # Manejo de movimientos en SQLite ├── config.json # ⚠️ Generado al usar la app, no subir ├── movements_log.db # ⚠️ Base de datos local, no subir ├── requirements.txt ├── Dockerfile # (opcional) para contenerizar la app └── README.md


---

## 🧰 Requisitos

- Python 3.9 o superior
- Streamlit
- psutil
- tabulate
- pandas

## Instala con:
pip install -r requirements.txt

# 🧪 Cómo usar (modo terminal)

## Ejecutar desde consola
- python app/cli.py --move-buffer    # Mueve al buffer si el disco está lleno
- python app/cli.py --archive        # Archiva desde buffer al cold storage
- python app/cli.py --all            # Ignora el umbral y hace ambos
- python app/cli.py --list           # Ver últimos archivos movidos
- La primera vez, se te pedirá que configures rutas y preferencias.

## 💻 Interfaz visual (Streamlit)
streamlit run app/dashboard.py

### Desde ahí podrás:

- Configurar rutas y parámetros
- Lanzar movimientos manuales
- Ver historial completo

## 🛡️ Archivos ignorados (en .gitignore)
config.json
movements_log.db
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml

## 📦 Envío automático (opcional)
Puedes programar el script con el Task Scheduler (Windows) o cron (Linux) para ejecutarlo cada X tiempo.
## Ejemplo programable:
python app/cli.py --move-buffer

## 🧪 Ideas para el futuro
- Notificaciones por correo o Telegram cuando se mueven archivos
- Panel para editar reglas por tipo o tamaño
- Sincronización con nube
- Autenticación para múltiples usuarios
- Soporte multi-plataforma (Linux, NAS)

## 🧑‍💻 Autor
Hecho con ❤️ por feliperosasgp
Proyecto abierto para contribuir y mejorar juntos 🚀

## 📜 Licencia
MIT License
