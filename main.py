from src.data_manager import DataManager
from src.repo_metrics import RepoMetrics
from src.batch_repo_metrics import BatchRepoMetrics
from src.batch_processor import BatchProcessor
from src.github_api import GitHubAPI
from src.dependency_analyzer import DependencyAnalyzer
from src.transform_data import transform_dependencies_to_columns
from src.config import GITHUB_TOKEN

def pipeline_processing():
    """
    Ejecuta el pipeline completo sin la Capa 3, ya que las métricas generales se añaden en la Capa 2.
    """
    print("🚀 Iniciando pipeline de procesamiento de repositorios...")

    # ---------------- Capa 0: Cargar Datos Originales ----------------
    input_file = "data/raw/repositories_raw_data.csv"
    capa_0_file = "data/processed/datos_capa_0.csv"
    print("\n📂 [Capa 0] Cargando datos originales...")
    data_manager = DataManager(input_file, capa_0_file)
    df = data_manager.load_data()
    data_manager.save_data(df)

    # ---------------- Capa 1: Agregar Lenguajes ----------------
    capa_1_file = "data/processed/datos_capa_1.csv"
    print("\n🖥️ [Capa 1] Agregando lenguajes...")
    repo_metrics = RepoMetrics(GITHUB_TOKEN)
    batch_processor = BatchRepoMetrics(repo_metrics)
    df = batch_processor.update_repository_metrics(df)
    data_manager = DataManager(capa_0_file, capa_1_file)
    data_manager.save_data(df)

    # ---------------- Capa 2: Extraer Dependencias y Métricas Generales ----------------
    capa_2_file = "data/processed/datos_capa_2.csv"
    print("\n🔍 [Capa 2] Analizando dependencias y métricas generales...")
    github_api = GitHubAPI(GITHUB_TOKEN)
    analyzer = DependencyAnalyzer(github_api)
    batch_processor = BatchProcessor(analyzer)
    df = batch_processor.process_dataframe(df)
    df = transform_dependencies_to_columns(df)
    data_manager = DataManager(capa_1_file, capa_2_file)
    data_manager.save_data(df)

    print(f"\n✅ Pipeline completado. Datos finales en {capa_2_file}")

if __name__ == "__main__":
    pipeline_processing()
