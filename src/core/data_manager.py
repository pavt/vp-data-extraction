import os
import pandas as pd
import numpy as np

class DataManager:
    def __init__(self, input_filepath, output_filepath):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def load_data(self) -> pd.DataFrame:
        """
        Carga el dataset, elimina columnas innecesarias y categoriza `vulnerability-proneness-all`.

        Returns:
            pd.DataFrame: DataFrame limpio con los datos cargados.
        """
        if not os.path.exists(self.input_filepath):
            raise FileNotFoundError(f"❌ Error: No se encontró el archivo {self.input_filepath}")

        df = pd.read_csv(self.input_filepath)

        # 1️⃣ Eliminar columnas innecesarias
        cols_to_drop = [
            'CWE Tags', 'topics', 'Low', 'Medium', 'High', 'Critical', 
            'Total Vulnerabilities', 'labels','commits'
        ]
        df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

        # 2️⃣ Aplicar categorización en `vulnerability-proneness-all`
        df = self.categorize_vp_equalfreq(df)

        # 3️⃣ Eliminar la columna temporal `log_vp`
        if "log_vp" in df.columns:
            df.drop(columns=["log_vp"], inplace=True)

        return df

    @staticmethod
    def categorize_vp_equalfreq(df):
        """
        Categoriza `vulnerability-proneness-all` en 3 niveles usando discretización con igual cantidad de muestras.

        Args:
            df (pd.DataFrame): DataFrame con la columna `vulnerability-proneness-all`.

        Returns:
            pd.DataFrame: DataFrame con la nueva columna `vp-category-equalfreq`.
        """
        df_temp = df.copy()

        # Evitar errores en log(0) añadiendo 1 antes de aplicar la transformación logarítmica
        df_temp["log_vp"] = np.log1p(df_temp["vulnerability-proneness-all"])

        # Discretización en 3 categorías de igual frecuencia
        df_temp["vp-category-equalfreq"] = pd.qcut(df_temp["log_vp"], q=3, labels=[0, 1, 2])

        return df_temp


    def save_data(self, df: pd.DataFrame):
        """
        Guarda el DataFrame en un archivo CSV.

        Args:
            df (pd.DataFrame): DataFrame a guardar.
        """
        os.makedirs(os.path.dirname(self.output_filepath), exist_ok=True)  # Crea la carpeta si no existe
        df.to_csv(self.output_filepath, index=False)
        print(f"✅ Datos guardados en {self.output_filepath}")
