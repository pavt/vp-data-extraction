import json
import base64
from typing import Dict, List, Optional
from .github_api import GitHubAPI

class DependencyAnalyzer:
    def __init__(self, github_api: GitHubAPI):
        """
        Analizador de dependencias de repositorios en GitHub.

        Args:
            github_api (GitHubAPI): Instancia de GitHubAPI para realizar peticiones.
        """
        self.github_api = github_api

    def get_package_json(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Obtiene el archivo package.json del repositorio.

        Args:
            owner (str): Propietario del repositorio.
            repo (str): Nombre del repositorio.

        Returns:
            Optional[Dict]: Contenido de package.json como diccionario o None si no se encuentra.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/package.json"
        content = self.github_api.get_json(url)
        
        if content and 'content' in content:
            try:
                return json.loads(base64.b64decode(content['content']).decode())
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"⚠️ Error decodificando package.json en {owner}/{repo}: {e}")
        return None

    def extract_dependencies(self, package_json: Dict) -> List[Dict]:
        """
        Extrae las dependencias de un archivo package.json.

        Args:
            package_json (Dict): Diccionario con el contenido de package.json.

        Returns:
            List[Dict]: Lista de dependencias en formato {'name': str, 'version': str, 'type': str}.
        """
        return [
            {'name': name, 'version': version, 'type': dep_type}
            for key, dep_type in [('dependencies', 'production'), ('devDependencies', 'development')]
            for name, version in package_json.get(key, {}).items()
        ]

    def get_dependency_graph(self, owner: str, repo: str) -> List[Dict]:
        """
        Obtiene las dependencias desde el Dependency Graph de GitHub.

        Args:
            owner (str): Propietario del repositorio.
            repo (str): Nombre del repositorio.

        Returns:
            List[Dict]: Lista de dependencias con información detallada.
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/dependency-graph/snapshots"
        graph_data = self.github_api.get_json(url)
        dependencies = []
        
        if graph_data:
            for snapshot in graph_data:
                for manifest in snapshot.get('manifests', {}).values():
                    dependencies.extend([
                        {
                            'name': dep.get('package', {}).get('name', 'unknown'),
                            'version': dep.get('metadata', {}).get('version', 'unknown'),
                            'type': 'direct' if dep.get('direct', False) else 'indirect',
                            'source': 'dependency_graph'
                        }
                        for dep in manifest.get('resolved', {}).get('dependencies', [])
                    ])
        
        return dependencies

    def analyze_repository(self, owner: str, repo: str) -> Dict:
        """
        Analiza un repositorio y extrae sus dependencias.

        Args:
            owner (str): Propietario del repositorio.
            repo (str): Nombre del repositorio.

        Returns:
            Dict: Resultado con dependencias extraídas y metadatos.
        """
        result = {
            'repository': f"{owner}/{repo}",
            'dependencies': [],
            'metadata': {
                'sources_checked': [],
                'total_dependencies': 0,
                'error': None
            }
        }

        try:
            # Intentar obtener package.json
            package_json = self.get_package_json(owner, repo)
            if package_json:
                result['metadata']['sources_checked'].append('package.json')
                result['dependencies'].extend(self.extract_dependencies(package_json))

            # Obtener dependencias del Dependency Graph
            result['dependencies'].extend(self.get_dependency_graph(owner, repo))
            
            # Eliminar duplicados manteniendo el primer valor encontrado
            seen = set()
            result['dependencies'] = [
                dep for dep in result['dependencies']
                if (dep['name'], dep['version']) not in seen and not seen.add((dep['name'], dep['version']))
            ]

            result['metadata']['total_dependencies'] = len(result['dependencies'])

        except Exception as e:
            result['metadata']['error'] = str(e)

        return result
