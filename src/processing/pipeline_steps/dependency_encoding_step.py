from src.processing.pipeline_steps.base_step import PipelineStep
from src.processing.strategies.dependency_encoding_strategy import DependencyEncodingStrategy
from src.utils.logger import logger


class DependencyEncodingStep(PipelineStep):
    """
    Paso del pipeline para aplicar One-Hot Encoding en la columna `dependencies_json`.
    """

    def __init__(self, input_path, output_path, next_step=None):
        super().__init__(next_step)
        self.strategy = DependencyEncodingStrategy(input_path, output_path)

    def process(self, df):
        logger.info("⚙️ Ejecutando One-Hot Encoding en dependencias...")
        return self.strategy.process(df)
