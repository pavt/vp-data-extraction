import pandas as pd
from src.processing.strategies.feature_engineering_strategy import FeatureEngineeringStrategy

class OneHotEncodingStrategy(FeatureEngineeringStrategy):
    """
    Estrategia de Feature Engineering para aplicar One-Hot Encoding a la columna 'Category'.
    """

    def apply_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica One-Hot Encoding a la columna 'Category'.

        Args:
            df (pd.DataFrame): DataFrame de entrada.

        Returns:
            pd.DataFrame: DataFrame con la columna 'Category' transformada.
        """
        if "Category" in df.columns:
            df = pd.get_dummies(df, columns=["Category"], prefix="cat", dtype=int)
        return df
