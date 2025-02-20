import pandas as pd
from src.config import GITHUB_TOKEN
from src.repo_metrics import RepoMetrics
from src.batch_repo_metrics import BatchRepoMetrics

if __name__ == "__main__":
    print("🚀 Iniciando análisis de repositorios...")

    df = pd.read_csv("data/raw/repositories_raw_data.csv")  # Nuevo nombre

    # Inicializar clases con registro de errores
    repo_metrics = RepoMetrics(GITHUB_TOKEN)
    batch_processor = BatchRepoMetrics(repo_metrics, error_log_path="data/raw/repositories_errors_log.csv")

    # Procesar repositorios
    df_with_metrics = batch_processor.update_repository_metrics(df)

    # Guardar resultados en la nueva estructura
    df_with_metrics.to_csv("data/processed/repositories_features_with_languages.csv", index=False)

    print(f"✅ Archivo actualizado: {len(df_with_metrics)} repos analizados.")
    lang_cols = [col for col in df_with_metrics.columns if col.startswith('lang_')]
    print(f"🗂 Total lenguajes detectados: {len(lang_cols)}")

    if len(batch_processor.errors) > 0:
        print(f"⚠️ Hubo {len(batch_processor.errors)} errores, revisa 'data/raw/repositories_errors_log.csv'.")
