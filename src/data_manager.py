import os
import pandas as pd

class DataManager:
    """
    Clase para manejar la carga, limpieza y guardado de datos en archivos CSV.
    """
    def __init__(self, input_filepath: str, output_filepath: str):
        """
        Inicializa la clase con las rutas de entrada y salida.

        Args:
            input_filepath (str): Ruta del archivo de entrada.
            output_filepath (str): Ruta del archivo de salida.
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath

    def load_data(self) -> pd.DataFrame:
        """
        Carga el dataset eliminando columnas innecesarias.

        Returns:
            pd.DataFrame: DataFrame limpio con los datos cargados.
        """
        if not os.path.exists(self.input_filepath):
            raise FileNotFoundError(f"❌ Error: No se encontró el archivo {self.input_filepath}")

        df = pd.read_csv(self.input_filepath)

        # Columnas a eliminar (verifica si existen antes de eliminarlas)
        cols_to_drop = [
            'labels', 'topics', 'Low', 'Medium', 'High', 'Critical', 
            'Total Vulnerabilities', 'CWE Tags', 'vulnerability-proneness-all'
        ]
        df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)

        return df

    def save_data(self, df: pd.DataFrame):
        """
        Guarda el DataFrame en un archivo CSV.

        Args:
            df (pd.DataFrame): DataFrame a guardar.
        """
        os.makedirs(os.path.dirname(self.output_filepath), exist_ok=True)  # Crea la carpeta si no existe
        df.to_csv(self.output_filepath, index=False)
        print(f"✅ Datos guardados en {self.output_filepath}")
