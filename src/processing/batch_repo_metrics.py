import time
import pandas as pd
from src.utils.logger import logger

from tqdm import tqdm
from src.utils.repo_metrics import RepoMetrics  # ✅ Ruta correcta después del cambio

class BatchRepoMetrics:
    """
    Procesa múltiples repositorios en paralelo para obtener métricas y guarda errores.
    """

    def __init__(self, repo_metrics: RepoMetrics, error_log_path: str = "data/logs/error_log_capa_1.csv"):
        self.repo_metrics = repo_metrics
        self.error_log_path = error_log_path
        self.errors = []  # ✅ Inicializar lista de errores


    def update_repository_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Itera sobre los repositorios en el DataFrame y obtiene métricas con paginación para commits.
        """
        logger.info("🔍 Actualizando métricas del repositorio...")

        commit_counts = []  # Lista para almacenar el conteo de commits

        for index, row in tqdm(df.iterrows(), total=len(df)):
            try:
                # Obtener las métricas del repositorio
                metrics = self.repo_metrics.get_repo_metrics(row["repo_owner"], row["repo_name"])

                if metrics:
                    for key, value in metrics.items():
                        df.at[index, key] = value  # Agregar métricas al DataFrame

                # Obtener número total de commits con paginación
                commit_count = self.repo_metrics.get_commit_count_paginated(row["repo_owner"], row["repo_name"])
                commit_counts.append(commit_count if commit_count is not None else 0)

            except Exception as e:
                logger.error(f"⚠️ Error actualizando métricas para {row['repo_owner']}/{row['repo_name']}: {e}")
                commit_counts.append(0)  # En caso de error, asignar 0 commits

        # Agregar la nueva columna al DataFrame
        df["commit_count"] = commit_counts
        logger.info("✅ Métricas del repositorio actualizadas correctamente.")
        
        return df