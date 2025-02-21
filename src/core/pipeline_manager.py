from src.core.processor_factory import ProcessorFactory
from src.core.pipeline_chain import PipelineChain
from src.utils.logger import logger
from src.processing.pipeline_steps.feature_engineering_step import FeatureEngineeringStep
from src.processing.strategies.dependency_encoding_strategy import DependencyEncodingStrategy
from src.processing.pipeline_steps.dependency_encoding_step import DependencyEncodingStep
from src.processing.pipeline_steps.license_encoding_step import LicenseEncodingStep
from src.processing.pipeline_steps.description_feature_engineering_step import DescriptionFeatureEngineeringStep  # ✅ Nueva capa
from src.processing.pipeline_steps.description_ngram_encoding_step import DescriptionNgramEncodingStep  # ✅ Nueva Capa 7


 

from src.core.data_manager import DataManager
from src.processing.batch_repo_metrics import BatchRepoMetrics
from src.processing.batch_processor import BatchProcessor
from src.processing.dependency_analyzer import DependencyAnalyzer
from src.core.github_api import GitHubAPI
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
            "capa_4": "data/processed/datos_capa_4.csv",
            "capa_5": "data/processed/datos_capa_5.csv",
            "capa_6": "data/processed/datos_capa_6.csv",  # ✅ Nueva capa para extracción de características en la descripción
            "capa_7": "data/processed/datos_capa_7.csv",  # ✅ Nueva capa para One-Hot Encoding en n-gramas

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
        df = self.encode_dependencies(df)  # ✅ Capa 4
        df = self.encode_license_name(df)  # ✅ Capa 5
        df = self.apply_description_feature_engineering(df)  # ✅ Nueva Capa 6
        df = self.encode_description_ngrams(df)  # ✅ Nueva Capa 7


        print(f"\n✅ Pipeline completado. Datos finales en {self.data_paths['capa_6']}")

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

        github_api = GitHubAPI(GITHUB_TOKEN)
        dependency_analyzer = DependencyAnalyzer(github_api)
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

    def encode_dependencies(self, df):
        """
        Capa 4: Aplicar One-Hot Encoding a la columna `dependencies_json`.
        """
        print("\n🛠️ [Capa 4] Aplicando One-Hot Encoding a dependencias...")

        step = DependencyEncodingStep(
            input_path=self.data_paths["capa_3"],
            output_path=self.data_paths["capa_4"]
        )

        df = step.process(df)

        data_manager = DataManager(self.data_paths["capa_3"], self.data_paths["capa_4"])
        data_manager.save_data(df)

        return df

    def encode_license_name(self, df):
        """
        Capa 5: Aplicar One-Hot Encoding en la columna `license_name`.
        """
        print("\n🛠️ [Capa 5] Aplicando One-Hot Encoding a license_name...")

        step = LicenseEncodingStep(
            input_path=self.data_paths["capa_4"],
            output_path=self.data_paths["capa_5"]
        )

        df = step.process(df)

        data_manager = DataManager(self.data_paths["capa_4"], self.data_paths["capa_5"])
        data_manager.save_data(df)

        return df

    def apply_description_feature_engineering(self, df):
        """
        Capa 6: Extraer características de la columna `description`.
        """
        print("\n🛠️ [Capa 6] Extrayendo características de la descripción...")

        step = DescriptionFeatureEngineeringStep(
            input_path=self.data_paths["capa_5"], 
            output_path=self.data_paths["capa_6"]
        )

        df = step.process(df)

        data_manager = DataManager(self.data_paths["capa_5"], self.data_paths["capa_6"])
        data_manager.save_data(df)

        return df

    def encode_description_ngrams(self, df):
        """
        Capa 7: Aplicar One-Hot Encoding a `desc_bigram_most_common` y `desc_trigram_most_common`.
        """
        print("\n🛠️ [Capa 7] Aplicando One-Hot Encoding a bigramas y trigramas...")

        step = DescriptionNgramEncodingStep(
            input_path=self.data_paths["capa_6"],
            output_path=self.data_paths["capa_7"]
        )

        df = step.process(df)

        data_manager = DataManager(self.data_paths["capa_6"], self.data_paths["capa_7"])
        data_manager.save_data(df)

        return df
