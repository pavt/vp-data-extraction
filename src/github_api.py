import requests
import json
import time
from typing import Dict, Optional, Any

class GitHubAPI:
    def __init__(self, token: str, rate_limit_pause: float = 0.5, max_retries: int = 3):
        """
        Cliente para interactuar con la API de GitHub.

        Args:
            token (str): Token de autenticación para la API de GitHub.
            rate_limit_pause (float, opcional): Pausa en segundos entre solicitudes para evitar límites de la API.
            max_retries (int, opcional): Número máximo de intentos en caso de fallo.
        """
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.rate_limit_pause = rate_limit_pause
        self.max_retries = max_retries

    def get_json(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Realiza una solicitud GET a la API de GitHub y devuelve la respuesta en formato JSON.

        Args:
            url (str): URL de la API de GitHub.

        Returns:
            Optional[Dict]: Respuesta en formato JSON o None si falla.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()  # Lanza una excepción si el código no es 2xx

                # GitHub retorna 204 en algunas respuestas vacías
                if response.status_code == 204:
                    return None

                return response.json()
            
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Error al acceder a {url}: {e} (Intento {attempt}/{self.max_retries})")
                time.sleep(self.rate_limit_pause)  # Esperar antes de reintentar
        
        print(f"❌ Fallo permanente al obtener datos de {url} tras {self.max_retries} intentos.")
        return None
