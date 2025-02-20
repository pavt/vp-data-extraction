import pandas as pd
from src.config import GITHUB_TOKEN
from src.github_api import GitHubAPI
from src.dependency_analyzer import DependencyAnalyzer
from src.batch_processor import BatchProcessor
from src.transform_data import transform_dependencies_to_columns

if __name__ == "__main__":
    df = pd.read_csv('data/github_repo_metrics_final.csv')
    df = df.drop(columns=['labels', 'topics', 'Low', 'Medium', 'High', 'Critical', 'Total Vulnerabilities', 'CWE Tags', 'vulnerability-proneness-all'])

    github_api = GitHubAPI(GITHUB_TOKEN)
    analyzer = DependencyAnalyzer(github_api)
    processor = BatchProcessor(analyzer)
    df_with_deps = processor.process_dataframe(df)

    df_final = transform_dependencies_to_columns(df_with_deps)
    df_final.to_csv('data/repos_dependencies_matrix.csv', index=False)

    print("Resumen final:")
    print(f"Total repositorios procesados: {len(df_final)}")
    print(f"Total dependencias únicas: {len([col for col in df_final.columns if col.startswith('dep_')])}")
    print(f"Repositorios con errores: {len(df_final[df_final['dep_error'].notna()])}")
