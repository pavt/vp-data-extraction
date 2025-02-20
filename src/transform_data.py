import json
import pandas as pd
from tqdm import tqdm

def transform_dependencies_to_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte la columna 'dependencies_json' en columnas individuales para cada dependencia.

    Args:
        df (pd.DataFrame): DataFrame con la columna 'dependencies_json'.

    Returns:
        pd.DataFrame: DataFrame con nuevas columnas representando la presencia de cada dependencia.
    """

    print("🔍 Transformando dependencias en columnas...")

    def get_dep_names_set(json_str):
        try:
            data = json.loads(json_str)
            return {dep['name'] for dep in data.get('dependencies', [])}
        except:
            return set()

    print("📊 Recolectando nombres únicos de dependencias...")
    all_dependencies = set()
    for _, row in tqdm(df.iterrows(), total=len(df)):
        all_dependencies.update(get_dep_names_set(row['dependencies_json']))

    print(f"✅ Se encontraron {len(all_dependencies)} dependencias únicas.")

    # 🚀 Creamos un DataFrame auxiliar en lugar de modificar `df` directamente
    dep_columns = {dep: [] for dep in all_dependencies}

    print("⚡ Creando matriz de dependencias...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        deps_set = get_dep_names_set(row['dependencies_json'])
        for dep in all_dependencies:
            dep_columns[dep].append(1 if dep in deps_set else 0)

    # Convertir el diccionario en un DataFrame
    dep_df = pd.DataFrame(dep_columns)

    # Ajustar nombres de columnas (evitar caracteres especiales)
    dep_df.columns = [f"dep_{col.replace('-', '_').replace('@', '').replace('/', '_')}" for col in dep_df.columns]

    # 🔗 Unir nuevo DataFrame con el original y evitar fragmentación
    df = pd.concat([df.reset_index(drop=True), dep_df], axis=1)

    print("✅ Transformación completada.")
    return df
