import pandas as pd
from src.processing.strategies.base_strategy import ProcessingStrategy
from src.utils.logger import logger

class LicenseEncodingStrategy(ProcessingStrategy):
    """
    Estrategia para aplicar One-Hot Encoding en la columna `license_name`.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("🔍 [Capa X] Aplicando One-Hot Encoding en licencias...")

        # Extraer todas las licencias únicas
        all_licenses = df["license_name"].dropna().unique()

        # Inicializar todas las nuevas columnas con 0
        for license in all_licenses:
            col_name = f"license_{license.replace(' ', '_').replace('-', '_')}"
            #df[col_name] = 0
            new_column = pd.DataFrame({col_name: 0}, index=df.index)
            df = pd.concat([df, new_column], axis=1)

        # Llenar las columnas con 1 si la licencia está presente
        for index, row in df.iterrows():
            if pd.notna(row["license_name"]):
                col_name = f"license_{row['license_name'].replace(' ', '_').replace('-', '_')}"
                df.at[index, col_name] = 1

        logger.info("✅ One-Hot Encoding de licencias completado.")
        return df
