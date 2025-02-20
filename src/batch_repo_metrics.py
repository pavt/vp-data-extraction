import time
import pandas as pd
from tqdm import tqdm
from src.repo_metrics import RepoMetrics

class BatchRepoMetrics:
    """
    Procesa múltiples repositorios en paralelo para obtener métricas y guarda errores.
    """

    def __init__(self, repo_metrics: RepoMetrics, error_log_path: str = "data/error_log.csv"):
        self.repo_metrics = repo_metrics
        self.error_log_path = error_log_path
        self.errors = []  # Lista para almacenar repositorios con errores

    def update_repository_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega columnas de métricas y lenguajes a un DataFrame con repositorios de GitHub.
        """
        all_languages = set()

        print("📊 Recolectando todos los posibles lenguajes en repositorios...")
        for index, row in tqdm(df.iterrows(), total=len(df)):
            try:
                metrics = self.repo_metrics.get_repo_metrics(row["repo_owner"], row["repo_name"])
                if metrics:
                    lang_cols = [col for col in metrics.keys() if col.startswith('lang_')]
                    all_languages.update(lang_cols)
                else:
                    raise ValueError("❌ Respuesta vacía de la API")
            except Exception as e:
                error_msg = f"{row['repo_owner']}/{row['repo_name']}: {str(e)}"
                print(f"⚠️ Error recolectando datos: {error_msg}")
                self.errors.append({"repo_owner": row["repo_owner"], "repo_name": row["repo_name"], "error": str(e)})
            time.sleep(self.repo_metrics.rate_limit_pause)

        # Inicializar columnas de idiomas con 0
        for lang_col in all_languages:
            df[lang_col] = 0

        print("\n🔍 Actualizando métricas y lenguajes en el DataFrame...")
        for index, row in tqdm(df.iterrows(), total=len(df)):
            try:
                metrics = self.repo_metrics.get_repo_metrics(row["repo_owner"], row["repo_name"])
                if metrics:
                    for key, value in metrics.items():
                        df.at[index, key] = value
                else:
                    raise ValueError("❌ No se obtuvieron métricas")
            except Exception as e:
                error_msg = f"{row['repo_owner']}/{row['repo_name']}: {str(e)}"
                print(f"⚠️ Error actualizando métricas: {error_msg}")
                self.errors.append({"repo_owner": row["repo_owner"], "repo_name": row["repo_name"], "error": str(e)})

            time.sleep(self.repo_metrics.rate_limit_pause)

        # Guardar errores en un CSV si hay errores
        if self.errors:
            error_df = pd.DataFrame(self.errors)
            error_df.to_csv(self.error_log_path, index=False)
            print(f"❌ Se guardaron {len(self.errors)} errores en '{self.error_log_path}'.")

        return df
