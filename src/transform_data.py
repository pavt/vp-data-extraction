import json
import pandas as pd
from tqdm import tqdm

def extract_dependency_names(json_str):
    """Extrae nombres de dependencias de una cadena JSON"""
    try:
        return {dep['name'] for dep in json.loads(json_str).get('dependencies', [])}
    except (TypeError, json.JSONDecodeError):
        return set()

def transform_dependencies_to_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte las dependencias de un JSON en columnas binarias en el DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame con una columna 'dependencies_json' que contiene JSON con dependencias.

    Returns:
        pd.DataFrame: DataFrame con columnas binarias para cada dependencia.
    """
    print("Transformando dependencias en columnas...")

    # Vectorización: Extrae dependencias en un solo paso
    tqdm.pandas()
    df["dependency_set"] = df["dependencies_json"].map(extract_dependency_names)

    # Obtener todos los nombres únicos de dependencias
    print("Recolectando nombres únicos de dependencias...")
    all_dependencies = set().union(*df["dependency_set"])

    print(f"Se encontraron {len(all_dependencies)} dependencias únicas")

    # Crear columnas binarias de dependencias
    print("Creando columnas binarias para cada dependencia...")
    for dep in tqdm(all_dependencies):
        col_name = f'dep_{dep.replace("-", "_").replace("@", "").replace("/", "_")}'
        df[col_name] = df["dependency_set"].map(lambda x: 1 if dep in x else 0)

    # Eliminar la columna temporal
    df.drop(columns=["dependency_set"], inplace=True)

    return df
