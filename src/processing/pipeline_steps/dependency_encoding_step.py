from src.processing.pipeline_steps.base_step import PipelineStep
from src.processing.strategies.dependency_encoding_strategy import DependencyEncodingStrategy
from src.core.data_manager import DataManager
from src.utils.logger import logger

class DependencyEncodingStep(PipelineStep):
    """
    Paso del pipeline para aplicar One-Hot Encoding en `dependencies_json`.
    """

    def __init__(self, input_path, output_path, next_step=None):
        super().__init__(output_path, next_step)  # ✅ Se agrega output_path
        self.strategy = DependencyEncodingStrategy(input_path, output_path)

    def process(self, df):
        logger.info("⚙️ Ejecutando DependencyEncodingStep...")
        return self.strategy.process(df)
