import json
import pandas as pd
from tqdm import tqdm

def transform_dependencies_to_columns(df: pd.DataFrame) -> pd.DataFrame:
    print("Transformando dependencias en columnas...")

    def get_dep_names_set(json_str):
        try:
            data = json.loads(json_str)
            return {dep['name'] for dep in data.get('dependencies', [])}
        except:
            return set()

    print("Recolectando nombres únicos de dependencias...")
    all_dependencies = set()
    for _, row in tqdm(df.iterrows(), total=len(df)):
        deps = get_dep_names_set(row['dependencies_json'])
        all_dependencies.update(deps)

    print(f"Se encontraron {len(all_dependencies)} dependencias únicas")

    print("Creando columnas para cada dependencia...")
    for dep in tqdm(all_dependencies):
        col_name = f'dep_{dep.replace("-", "_").replace("@", "").replace("/", "_")}'
        df[col_name] = df['dependencies_json'].apply(lambda x: 1 if dep in get_dep_names_set(x) else 0)

    return df
