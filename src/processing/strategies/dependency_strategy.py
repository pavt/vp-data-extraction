from .base_strategy import ProcessingStrategy
from src.core.github_api import GitHubAPI
from src.processing.batch_processor import BatchProcessor
from src.processing.dependency_analyzer import DependencyAnalyzer
from src.utils.transform_data import transform_dependencies_to_columns
from src.core.data_manager import DataManager
from src.config import GITHUB_TOKEN
from src.utils.logger import logger

class DependencyProcessingStrategy(ProcessingStrategy):
    """
    Estrategia para extraer dependencias y métricas generales (Capa 2).
    """

    def process(self, df):
        logger.info("🔍 [Capa 2] Extrayendo dependencias y métricas...")
        
        github_api = GitHubAPI(GITHUB_TOKEN)
        analyzer = DependencyAnalyzer(github_api)
        batch_processor = BatchProcessor(analyzer)

        df = batch_processor.process_dataframe(df)  # 🔹 Extrae dependencias
        data_manager = DataManager(self.input_path, self.output_path)
        data_manager.save_data(df)

        return df
