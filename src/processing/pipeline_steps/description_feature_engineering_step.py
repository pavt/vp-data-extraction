from src.processing.pipeline_steps.base_step import PipelineStep
from src.processing.strategies.description_feature_engineering_strategy import DescriptionFeatureEngineeringStrategy
from src.core.data_manager import DataManager
from src.utils.logger import logger

class DescriptionFeatureEngineeringStep(PipelineStep):
    """
    Paso del pipeline para extraer características de la columna `description`.
    """

    def __init__(self, input_path, output_path, next_step=None):
        super().__init__(input_path, output_path, next_step)  # ✅ Se usa la nueva versión con next_step opcional
        self.strategy = DescriptionFeatureEngineeringStrategy()

    def process(self, df):
        logger.info("⚙️ Ejecutando DescriptionFeatureEngineeringStep...")
        df = self.strategy.process(df)
        return df if not self.next_step else self.next_step.process(df)  # ✅ Propaga el procesamiento al siguiente paso si existe
