import pandas as pd
import re
from src.processing.strategies.base_strategy import ProcessingStrategy
from src.utils.logger import logger

class DescriptionNgramEncodingStrategy(ProcessingStrategy):
    """
    Estrategia para aplicar One-Hot Encoding en las columnas `desc_bigram_most_common` y `desc_trigram_most_common`.
    """

    def __init__(self, input_path, output_path):
        super().__init__(input_path, output_path)  # ✅ Agrega los parámetros obligatorios

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("🔍 [Capa 7] Aplicando One-Hot Encoding en bigramas y trigramas...")

        # Lista de columnas a codificar
        columns_to_encode = ["desc_bigram_most_common", "desc_trigram_most_common"]

        for col in columns_to_encode:
            if col in df.columns:
                # Asegurar nombres de columnas sin caracteres especiales
                df[col] = df[col].fillna("UNKNOWN")  # Reemplaza NaN con 'UNKNOWN'
                df[col] = df[col].apply(lambda x: re.sub(r'\W+', '_', x))  # Sustituye caracteres no alfanuméricos por '_'

                # Aplicar One-Hot Encoding
                encoded_df = pd.get_dummies(df[col], prefix=col, dtype=int)

                # Concatenar con el DataFrame original
                df = pd.concat([df, encoded_df], axis=1)

                # Eliminar la columna original
                df.drop(columns=[col], inplace=True)

        logger.info("✅ One-Hot Encoding aplicado en bigramas y trigramas.")
        return df
