from .base_strategy import ProcessingStrategy  # ✅ Importación relativa correcta

from src.processing.strategies.base_strategy import ProcessingStrategy
from src.utils.repo_metrics import RepoMetrics
from src.processing.batch_repo_metrics import BatchRepoMetrics
from src.core.data_manager import DataManager
from src.config import GITHUB_TOKEN
from src.utils.logger import logger

class LanguageProcessingStrategy(ProcessingStrategy):
    """
    Estrategia para extraer lenguajes de los repositorios.
    """

    def process(self, df):
        logger.info("📊 [Capa 1] Extrayendo lenguajes...")
        repo_metrics = BatchRepoMetrics(RepoMetrics(GITHUB_TOKEN))
        df = repo_metrics.update_repository_metrics(df)
        data_manager = DataManager(self.input_path, self.output_path)
        data_manager.save_data(df)
        return df
