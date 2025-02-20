import json
import base64
from typing import Dict, List, Optional
from .github_api import GitHubAPI

class DependencyAnalyzer:
    def __init__(self, github_api: GitHubAPI):
        self.github_api = github_api

    def get_package_json(self, owner: str, repo: str) -> Optional[Dict]:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/package.json"
        content = self.github_api.get_json(url)
        if content and 'content' in content:
            return json.loads(base64.b64decode(content['content']).decode())
        return None

    def get_dependencies_from_package(self, package_json: Dict) -> List[Dict]:
        dependencies = []
        for name, version in package_json.get('dependencies', {}).items():
            dependencies.append({'name': name, 'version': version, 'type': 'production'})

        for name, version in package_json.get('devDependencies', {}).items():
            dependencies.append({'name': name, 'version': version, 'type': 'development'})

        return dependencies

    def analyze_repository(self, owner: str, repo: str) -> Dict:
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
            package_json = self.get_package_json(owner, repo)
            if package_json:
                result['metadata']['sources_checked'].append('package.json')
                result['dependencies'].extend(self.get_dependencies_from_package(package_json))

            result['metadata']['total_dependencies'] = len(result['dependencies'])

        except Exception as e:
            result['metadata']['error'] = str(e)

        return result
