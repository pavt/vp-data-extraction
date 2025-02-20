from src.core.processor_factory import ProcessorFactory
from src.core.pipeline_chain import PipelineChain
from src.utils.logger import logger
from src.processing.pipeline_steps.feature_engineering_step import FeatureEngineeringStep
from src.core.data_manager import DataManager
from src.processing.batch_repo_metrics import BatchRepoMetrics
from src.processing.batch_processor import BatchProcessor
from src.processing.dependency_analyzer import DependencyAnalyzer
from src.core.github_api import GitHubAPI  # ✅ Asegurar que se importa correctamente
from src.utils.repo_metrics import RepoMetrics
from src.config import GITHUB_TOKEN

class PipelineManager:
    """
    Administra el flujo de ejecución del pipeline.
    """

    def __init__(self, raw_data_path: str):
        """
        Inicializa la gestión del pipeline con rutas de datos.
        """
        self.raw_data_path = raw_data_path

        self.data_paths = {
            "capa_0": "data/processed/datos_capa_0.csv",
            "capa_1": "data/processed/datos_capa_1.csv",
            "capa_2": "data/processed/datos_capa_2.csv",
            "capa_3": "data/processed/datos_capa_3.csv",
        }

    def run(self):
        """
        Ejecuta el pipeline completo paso a paso en el orden correcto.
        """
        print("🚀 Iniciando pipeline de procesamiento de repositorios...")

        df = self.load_data()  # ✅ Capa 0
        df = self.extract_languages(df)  # ✅ Capa 1
        df = self.extract_dependencies_and_metrics(df)  # ✅ Capa 2
        df = self.apply_feature_engineering(df)  # ✅ Capa 3

        print(f"\n✅ Pipeline completado. Datos finales en {self.data_paths['capa_3']}")

    def load_data(self):
        """
        Carga los datos desde el archivo original (Capa 0).
        """
        logger.info("\n📂 [Capa 0] Cargando datos originales...")
        data_manager = DataManager(self.raw_data_path, self.data_paths["capa_0"])
        df = data_manager.load_data()
        data_manager.save_data(df)
        return df

    def extract_languages(self, df):
        """
        Capa 1: Extraer lenguajes de los repositorios.
        """
        print("\n🖥️ [Capa 1] Agregando lenguajes...")

        repo_metrics = BatchRepoMetrics(RepoMetrics(GITHUB_TOKEN))

        df = repo_metrics.update_repository_metrics(df)
        data_manager = DataManager(self.data_paths["capa_0"], self.data_paths["capa_1"])
        data_manager.save_data(df)
        return df

    def extract_dependencies_and_metrics(self, df):
        """
        Capa 2: Extraer dependencias y métricas generales.
        """
        print("\n🔍 [Capa 2] Analizando dependencias y métricas generales...")

        github_api = GitHubAPI(GITHUB_TOKEN)  # ✅ Crear instancia de GitHubAPI
        dependency_analyzer = DependencyAnalyzer(github_api)  # ✅ Pasar `github_api`
        batch_processor = BatchProcessor(dependency_analyzer)

        df = batch_processor.process_dataframe(df)
        data_manager = DataManager(self.data_paths["capa_1"], self.data_paths["capa_2"])
        data_manager.save_data(df)

        return df

    def apply_feature_engineering(self, df):
        """
        Capa 3: Aplicar Feature Engineering a los datos.
        """
        print("\n🛠️ [Capa 3] Aplicando Feature Engineering...")

        step = FeatureEngineeringStep(
            strategy_name="one_hot_encoding",
            input_path=self.data_paths["capa_2"],
            output_path=self.data_paths["capa_3"]
        )

        df = step.process(df)

        data_manager = DataManager(self.data_paths["capa_2"], self.data_paths["capa_3"])
        data_manager.save_data(df)

        return df
