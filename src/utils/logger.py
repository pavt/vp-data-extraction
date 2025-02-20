import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Crear carpeta de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configuración básica del logger
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",  # Añadir logs en vez de sobrescribir
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,  # Cambiar a DEBUG si necesitas más detalles
)

# Crear un logger para uso en otros módulos
logger = logging.getLogger("RepoMetrics")
