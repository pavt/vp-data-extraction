import sys
import os

# 🔹 Asegurar que src/ está en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.core.data_manager import DataManager
from src.core.github_api import GitHubAPI
from src.utils.repo_metrics import RepoMetrics  # ✅ Nueva ubicación


from src.processing.batch_repo_metrics import BatchRepoMetrics
from src.processing.batch_processor import BatchProcessor
from src.processing.dependency_analyzer import DependencyAnalyzer
from src.utils.transform_data import transform_dependencies_to_columns
from src.config import GITHUB_TOKEN


class PipelineManager:
    """
    Clase para gestionar el pipeline de procesamiento de datos de repositorios.
    """

    def __init__(self):
        self.data_paths = {
            "capa_0": "data/processed/datos_capa_0.csv",
            "capa_1": "data/processed/datos_capa_1.csv",
            "capa_2": "data/processed/datos_capa_2.csv",
        }

    def run(self):
        """
        Ejecuta el pipeline completo paso a paso.
        """
        print("🚀 Iniciando pipeline de procesamiento de repositorios...")

        df = self.load_data()
        df = self.extract_languages(df)
        df = self.extract_dependencies_and_metrics(df)

        print(f"\n✅ Pipeline completado. Datos finales en {self.data_paths['capa_2']}")

    def load_data(self):
        """
        Capa 0: Cargar datos originales.
        """
        input_file = "data/raw/repositories_raw_data.csv"
        print("\n📂 [Capa 0] Cargando datos originales...")
        data_manager = DataManager(input_file, self.data_paths["capa_0"])
        df = data_manager.load_data()
        data_manager.save_data(df)
        return df

    def extract_languages(self, df):
        """
        Capa 1: Extraer lenguajes de los repositorios.
        """
        print("\n🖥️ [Capa 1] Agregando lenguajes...")

        repo_metrics = BatchRepoMetrics(RepoMetrics(GITHUB_TOKEN))  # ✅


        df = repo_metrics.update_repository_metrics(df)
        data_manager = DataManager(self.data_paths["capa_0"], self.data_paths["capa_1"])
        data_manager.save_data(df)
        return df

    def extract_dependencies_and_metrics(self, df):
        """
        Capa 2: Extraer dependencias y métricas generales.
        """
        print("\n🔍 [Capa 2] Analizando dependencias y métricas generales...")
        github_api = GitHubAPI(GITHUB_TOKEN)
        analyzer = DependencyAnalyzer(github_api)
        batch_processor = BatchProcessor(analyzer)
        df = batch_processor.process_dataframe(df)
        df = transform_dependencies_to_columns(df)
        data_manager = DataManager(self.data_paths["capa_1"], self.data_paths["capa_2"])
        data_manager.save_data(df)
        return df

if __name__ == "__main__":
    pipeline = PipelineManager()
    pipeline.run()
