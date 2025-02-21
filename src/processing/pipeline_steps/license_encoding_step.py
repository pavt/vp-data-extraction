from src.processing.pipeline_steps.base_step import PipelineStep
from src.processing.strategies.license_encoding_strategy import LicenseEncodingStrategy
from src.core.data_manager import DataManager
from src.utils.logger import logger

class LicenseEncodingStep(PipelineStep):
    """
    Paso del pipeline para aplicar One-Hot Encoding en `license_name`.
    """

    def __init__(self, input_path, output_path, next_step=None):
        super().__init__(output_path, next_step)  # ✅ Ahora pasamos `output_path`
        self.strategy = LicenseEncodingStrategy(input_path, output_path)

    def process(self, df):
        logger.info("⚙️ Ejecutando LicenseEncodingStep...")
        return self.strategy.process(df)
