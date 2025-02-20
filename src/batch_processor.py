import json
import time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.dependency_analyzer import DependencyAnalyzer

class BatchProcessor:
    def __init__(self, analyzer: DependencyAnalyzer, max_workers: int = 5):
        self.analyzer = analyzer
        self.max_workers = max_workers

    def process_dataframe(self, df: pd.DataFrame, owner_col: str = 'repo_owner', repo_col: str = 'repo_name') -> pd.DataFrame:
        """
        Procesa un DataFrame de repositorios para obtener solo sus dependencias.
        """
        df_copy = df.copy()
        jobs = list(zip(df_copy[owner_col], df_copy[repo_col]))
        
        df_copy['dependencies_json'] = ''
        df_copy['dep_count'] = 0
        df_copy['dep_error'] = None

        with tqdm(total=len(jobs), desc="🔍 Analizando dependencias") as pbar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_repo = {
                    executor.submit(self.analyzer.analyze_repository, owner, repo): (owner, repo)
                    for owner, repo in jobs
                }

                for future in as_completed(future_to_repo):
                    owner, repo = future_to_repo[future]
                    try:
                        json_result = future.result()
                        idx = df_copy[
                            (df_copy[owner_col] == owner) & (df_copy[repo_col] == repo)
                        ].index[0]

                        df_copy.at[idx, 'dependencies_json'] = json.dumps(json_result, ensure_ascii=False)
                        df_copy.at[idx, 'dep_count'] = json_result['metadata']['total_dependencies']
                        df_copy.at[idx, 'dep_error'] = json_result['metadata'].get('error')

                    except Exception as e:
                        print(f"\n⚠️ Error procesando {owner}/{repo}: {str(e)}")
                        df_copy.at[idx, 'dep_error'] = str(e)

                    pbar.update(1)
                    time.sleep(0.5)

        return df_copy
