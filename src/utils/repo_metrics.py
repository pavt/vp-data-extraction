import requests
import time
from typing import Dict, Optional
from src.config import GITHUB_TOKEN
from src.utils.logger import logger  # ✅ Importar el logger

GRAPHQL_URL = "https://api.github.com/graphql"
REST_API_URL = "https://api.github.com"

class RepoMetrics:
    def __init__(self, token: str = GITHUB_TOKEN, rate_limit_pause: float = 1.0):
        self.token = token
        self.rate_limit_pause = rate_limit_pause
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.graphql_headers = {  # ✅ Ahora está definido correctamente
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def fetch_paginated_data(self, url: str) -> list:
        """
        Obtiene datos paginados de la API de GitHub, siguiendo el enlace `next`.
        """
        results = []
        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                results.extend(response.json())  # Agregar los datos actuales
                # Manejar el header `Link` para seguir la paginación
                link_header = response.headers.get("Link", "")
                next_url = None
                for link in link_header.split(","):
                    if 'rel="next"' in link:
                        next_url = link[link.find("<") + 1 : link.find(">")]
                        break
                url = next_url  # Continuar con la siguiente página
            else:
                logger.error(f"⚠️ Error obteniendo datos paginados: {response.status_code} - {response.text}")
                break
        return results

    def get_rest_api_data(self, owner: str, repo: str) -> Dict:
        """
        Obtiene métricas básicas del repositorio desde la API REST de GitHub con paginación.
        """
        try:
            repo_url = f"{REST_API_URL}/repos/{owner}/{repo}"
            response = requests.get(repo_url, headers=self.headers)
            if response.status_code != 200:
                logger.warning(f"⚠️ No se pudo obtener repo {owner}/{repo}: {response.status_code}")
                return {}

            repo_data = response.json()

            languages_url = f"{REST_API_URL}/repos/{owner}/{repo}/languages"
            languages_data = self.fetch_paginated_data(languages_url)

            return {
                "network_count": repo_data.get("network_count"),
                "subscribers_count": repo_data.get("subscribers_count"),
                "languages": languages_data  # ✅ Ahora obtenemos TODOS los lenguajes
            }
        except Exception as e:
            logger.error(f"⚠️ Error obteniendo datos REST para {owner}/{repo}: {e}")
            return {}

    def get_repo_metrics(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Obtiene información del repositorio usando GraphQL y REST API con paginación.
        """
        query = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            description
            primaryLanguage { name }
            licenseInfo { name }
            languages(first: 100, orderBy: {field: SIZE, direction: DESC}) {
              nodes { name }
            }
            stargazers { totalCount }
            isSecurityPolicyEnabled
            hasVulnerabilityAlertsEnabled
          }
        }
        """
        try:
            response = requests.post(
                GRAPHQL_URL,
                json={"query": query, "variables": {"owner": owner, "repo": repo}},
                headers=self.graphql_headers,
            )
            data = response.json()

            if "errors" in data:
                logger.warning(f"⚠️ GraphQL Error en {owner}/{repo}: {data['errors']}")
                return None

            if "data" not in data or data["data"]["repository"] is None:
                logger.warning(f"⚠️ No hay datos para {owner}/{repo}")
                return None

            repo_data = data["data"]["repository"]
            rest_data = self.get_rest_api_data(owner, repo)

            # Extraer idiomas desde GraphQL
            all_languages = [lang["name"] for lang in repo_data.get("languages", {}).get("nodes", [])]

            # Construir diccionario de métricas
            metrics = {
                "description": repo_data.get("description"),
                "primary_language": repo_data.get("primaryLanguage", {}).get("name"),
                "license_name": repo_data.get("licenseInfo", {}).get("name"),
                "security_policy_enabled": repo_data.get("isSecurityPolicyEnabled"),
                "vulnerability_alerts_enabled": repo_data.get("hasVulnerabilityAlertsEnabled"),
                "stargazers_count": repo_data["stargazers"]["totalCount"] if repo_data.get("stargazers") else 0,
            }

            # Agregar datos REST
            metrics.update(rest_data)

            # Agregar idiomas como columnas
            for lang in all_languages:
                col_name = f"lang_{lang.lower().replace(' ', '_').replace('-', '_').replace('+', 'plus')}"
                metrics[col_name] = 1

            return metrics

        except Exception as e:
            logger.error(f"⚠️ Error procesando {owner}/{repo}: {e}")
            return None
