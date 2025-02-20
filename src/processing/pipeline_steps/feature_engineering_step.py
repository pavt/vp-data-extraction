import pandas as pd
from src.processing.factories.feature_engineering_factory import FeatureEngineeringFactory
from src.core.pipeline_chain import PipelineStep
from src.utils.logger import logger

class FeatureEngineeringStep(PipelineStep):
    """
    Paso del pipeline que aplica una estrategia de Feature Engineering.
    """

    def __init__(self, strategy_name: str, input_path: str, output_path: str, next_step=None):
        super().__init__(next_step)
        self.strategy = FeatureEngineeringFactory.get_strategy(strategy_name)
        self.input_path = input_path
        self.output_path = output_path

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica la estrategia de Feature Engineering seleccionada.

        Args:
            df (pd.DataFrame): DataFrame de entrada.

        Returns:
            pd.DataFrame: DataFrame transformado.
        """
        logger.info(f"⚙️ Aplicando Feature Engineering con {self.strategy.__class__.__name__}...")
        df_transformed = self.strategy.apply_transformation(df)
        return df_transformed
