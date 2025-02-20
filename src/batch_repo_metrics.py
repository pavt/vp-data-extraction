import time
import pandas as pd
from tqdm import tqdm
from .repo_metrics import RepoMetrics

class BatchRepoMetrics:
    """
    Procesa múltiples repositorios en paralelo para obtener métricas.
    """

    def __init__(self, repo_metrics: RepoMetrics):
        self.repo_metrics = repo_metrics

    def update_repository_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega columnas de métricas y lenguajes a un DataFrame con repositorios de GitHub.
        """

        all_languages = set()

        print("📊 Recolectando todos los posibles lenguajes en repositorios...")
        for _, row in tqdm(df.iterrows(), total=len(df)):
            metrics = self.repo_metrics.get_repo_metrics(row["repo_owner"], row["repo_name"])
            if metrics:
                lang_cols = [col for col in metrics.keys() if col.startswith('lang_')]
                all_languages.update(lang_cols)
            time.sleep(self.repo_metrics.rate_limit_pause)

        # Inicializar columnas de idiomas con 0
        for lang_col in all_languages:
            df[lang_col] = 0

        print("\n🔍 Actualizando métricas y lenguajes en el DataFrame...")
        for _, row in tqdm(df.iterrows(), total=len(df)):
            metrics = self.repo_metrics.get_repo_metrics(row["repo_owner"], row["repo_name"])
            if metrics:
                for key, value in metrics.items():
                    df.at[_, key] = value

            time.sleep(self.repo_metrics.rate_limit_pause)

        return df
