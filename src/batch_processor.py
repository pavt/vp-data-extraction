import json
import time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .dependency_analyzer import DependencyAnalyzer

class BatchProcessor:
    def __init__(self, analyzer: DependencyAnalyzer, max_workers: int = 5, rate_limit_pause: float = 0.5):
        """
        Procesador en batch para analizar múltiples repositorios en paralelo.

        Args:
            analyzer (DependencyAnalyzer): Instancia del analizador de dependencias.
            max_workers (int, opcional): Número de hilos para el procesamiento concurrente.
            rate_limit_pause (float, opcional): Pausa entre solicitudes para evitar límites de la API.
        """
        self.analyzer = analyzer
        self.max_workers = max_workers
        self.rate_limit_pause = rate_limit_pause

    def process_repositories(self, df: pd.DataFrame, owner_col: str = 'repo_owner', repo_col: str = 'repo_name') -> pd.DataFrame:
        """
        Procesa una lista de repositorios obteniendo sus dependencias y guardándolas en el DataFrame.

        Args:
            df (pd.DataFrame): DataFrame con columnas 'repo_owner' y 'repo_name'.
            owner_col (str, opcional): Nombre de la columna con el propietario del repositorio.
            repo_col (str, opcional): Nombre de la columna con el nombre del repositorio.

        Returns:
            pd.DataFrame: DataFrame actualizado con las dependencias extraídas.
        """
        df_copy = df.copy()

        # Inicializar columnas con valores predeterminados
        df_copy = df_copy.assign(
            dependencies_json='',
            dep_count=0,
            dep_error=None
        )

        # Extraer tuplas de (owner, repo) y remover duplicados
        jobs = df_copy[[owner_col, repo_col]].drop_duplicates().itertuples(index=False, name=None)

        print(f"Procesando {len(jobs)} repositorios en paralelo con {self.max_workers} hilos...")

        with tqdm(total=len(jobs), desc="Analyzing repositories") as pbar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_repo = {executor.submit(self.analyzer.analyze_repository, owner, repo): (owner, repo) for owner, repo in jobs}

                for future in as_completed(future_to_repo):
                    owner, repo = future_to_repo[future]
                    try:
                        result = future.result()
                        result_json = json.dumps(result, ensure_ascii=False)
                        metadata = result.get('metadata', {})

                        # Localizar la fila correspondiente en el DataFrame
                        mask = (df_copy[owner_col] == owner) & (df_copy[repo_col] == repo)
                        df_copy.loc[mask, ['dependencies_json', 'dep_count', 'dep_error']] = [
                            result_json,
                            metadata.get('total_dependencies', 0),
                            metadata.get('error')
                        ]


