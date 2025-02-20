
# src/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener el token desde la variable de entorno
GITHUB_TOKEN = os.getenv("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")
