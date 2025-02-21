import pandas as pd
import json
from src.processing.strategies.base_strategy import ProcessingStrategy
from src.utils.logger import logger

class DependencyEncodingStrategy(ProcessingStrategy):
    """
    Estrategia para aplicar One-Hot Encoding en la columna `dependencies_json` (Capa 4).
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("🔍 [Capa 4] Aplicando One-Hot Encoding en dependencias...")

        all_dependencies = set()

        # Extraer todas las dependencias únicas correctamente
        for deps in df["dependencies_json"].dropna():
            try:
                deps_dict = json.loads(deps) if isinstance(deps, str) else deps
                dep_list = deps_dict.get("dependencies", [])  # Asegurar que obtenemos la lista de dependencias
                dep_names = [dep["name"] for dep in dep_list if "name" in dep]
                all_dependencies.update(dep_names)
            except Exception as e:
                logger.warning(f"⚠️ Error procesando dependencias: {e}")

        # Inicializar todas las nuevas columnas con 0
        for dep in all_dependencies:
            col_name = f"dep_{dep.replace('@', '').replace('/', '_')}"  # Evitar caracteres inválidos
            df[col_name] = 0

        # Llenar las columnas con 1 si la dependencia está presente
        for index, row in df.iterrows():
            try:
                if pd.notna(row["dependencies_json"]):
                    deps_dict = json.loads(row["dependencies_json"]) if isinstance(row["dependencies_json"], str) else row["dependencies_json"]
                    dep_list = deps_dict.get("dependencies", [])  # Acceder correctamente a las dependencias
                    dep_names = [dep["name"] for dep in dep_list if "name" in dep]
                    for dep in dep_names:
                        col_name = f"dep_{dep.replace('@', '').replace('/', '_')}"
                        df.at[index, col_name] = 1
            except Exception as e:
                logger.warning(f"⚠️ Error llenando columnas para índice {index}: {e}")

        logger.info("✅ One-Hot Encoding de dependencias completado.")
        return df
