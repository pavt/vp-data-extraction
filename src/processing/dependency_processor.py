from src.core.github_api import GitHubAPI
from src.processing.batch_processor import BatchProcessor
from src.processing.dependency_analyzer import DependencyAnalyzer
from src.utils.transform_data import transform_dependencies_to_columns
from src.core.data_manager import DataManager
from src.config import GITHUB_TOKEN
from src.utils.logger import logger

class DependencyProcessor:
    """
    Clase encargada de extraer dependencias y métricas generales (Capa 2).
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.github_api = GitHubAPI(GITHUB_TOKEN)
        self.analyzer = DependencyAnalyzer(self.github_api)
        self.batch_processor = BatchProcessor(self.analyzer)

    def process(self, df):
        """
        Ejecuta la extracción de dependencias y métricas generales.
        """
        try:
            logger.info("🔍 Iniciando extracción de dependencias y métricas...")
            df = self.batch_processor.process_dataframe(df)
            df = transform_dependencies_to_columns(df)
            data_manager = DataManager(self.input_path, self.output_path)
            data_manager.save_data(df)
            logger.info("✅ Extracción de dependencias completada.")
            return df
        except Exception as e:
            logger.error(f"❌ Error en extracción de dependencias: {e}")
            return df  # Devuelve el DataFrame original en caso de error
