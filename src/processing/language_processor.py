from src.utils.repo_metrics import RepoMetrics
from src.processing.batch_repo_metrics import BatchRepoMetrics
from src.core.data_manager import DataManager
from src.config import GITHUB_TOKEN
from src.utils.logger import logger

class LanguageProcessor:
    """
    Clase encargada de extraer los lenguajes de los repositorios (Capa 1).
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.repo_metrics = BatchRepoMetrics(RepoMetrics(GITHUB_TOKEN))

    def process(self, df):
        """
        Ejecuta la extracción de lenguajes y guarda los resultados.
        """
        try:
            logger.info("📊 Iniciando extracción de lenguajes...")
            df = self.repo_metrics.update_repository_metrics(df)
            data_manager = DataManager(self.input_path, self.output_path)
            data_manager.save_data(df)
            logger.info("✅ Extracción de lenguajes completada.")
            return df
        except Exception as e:
            logger.error(f"❌ Error en extracción de lenguajes: {e}")
            return df  # Devuelve el DataFrame original en caso de error
