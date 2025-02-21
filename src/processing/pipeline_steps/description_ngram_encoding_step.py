from src.processing.pipeline_steps.base_step import PipelineStep
from src.processing.strategies.description_ngram_encoding_strategy import DescriptionNgramEncodingStrategy
from src.core.data_manager import DataManager
from src.utils.logger import logger

class DescriptionNgramEncodingStep(PipelineStep):
    """
    Paso del pipeline para aplicar One-Hot Encoding en bigramas y trigramas.
    """

    def __init__(self, input_path, output_path, next_step=None):
        super().__init__(input_path, output_path, next_step)
        self.strategy = DescriptionNgramEncodingStrategy(input_path, output_path)  # ✅ Se añaden input_path y output_path

    def process(self, df):
        logger.info("⚙️ Ejecutando DescriptionNgramEncodingStep...")
        return self.strategy.process(df)
