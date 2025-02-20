import pandas as pd
from src.config import GITHUB_TOKEN
from src.repo_metrics import RepoMetrics
from src.batch_repo_metrics import BatchRepoMetrics

if __name__ == "__main__":
    print("🚀 Iniciando análisis de repositorios...")

    df = pd.read_csv("data/repos_dependencies_matrix.csv")

    # Inicializar clases
    repo_metrics = RepoMetrics(GITHUB_TOKEN)
    batch_processor = BatchRepoMetrics(repo_metrics)

    # Procesar repositorios
    df_with_metrics = batch_processor.update_repository_metrics(df)

    # Guardar resultados
    df_with_metrics.to_csv("data/github_repos_with_languages.csv", index=False)

    print(f"✅ Archivo actualizado: {len(df_with_metrics)} repos analizados.")
    lang_cols = [col for col in df_with_metrics.columns if col.startswith('lang_')]
    print(f"🗂 Total lenguajes detectados: {len(lang_cols)}")
