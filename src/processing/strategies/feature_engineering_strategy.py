from abc import ABC, abstractmethod
import pandas as pd

class FeatureEngineeringStrategy(ABC):
    """
    Interfaz base para todas las estrategias de Feature Engineering.
    """

    @abstractmethod
    def apply_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica la transformación al DataFrame.

        Args:
            df (pd.DataFrame): DataFrame de entrada.

        Returns:
            pd.DataFrame: DataFrame con la transformación aplicada.
        """
        pass
