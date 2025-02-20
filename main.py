import pandas as pd
from src.config import GITHUB_TOKEN
from src.github_api import GitHubAPI
from src.dependency_analyzer import DependencyAnalyzer
from src.batch_processor import BatchProcessor
from src.transform_data import transform_dependencies_to_columns
from src.data_manager import DataManager  # Nueva clase importada

# Definir rutas de entrada y salida
INPUT_CSV = "data/github_repo_metrics_final.csv"
OUTPUT_CSV = "data/repos_dependencies_matrix.csv"

def main():
    """Función principal para ejecutar el análisis de dependencias en repositorios."""
    try:
        print("🚀 Iniciando análisis de datos...")

        # Instanciar el manejador de datos
        data_manager = DataManager(INPUT_CSV, OUTPUT_CSV)

        print("🔍 Cargando datos...")
        df = data_manager.load_data()

        print("📡 Consultando dependencias en GitHub...")
        github_api = GitHubAPI(GITHUB_TOKEN)
        analyzer = DependencyAnalyzer(github_api)
        processor = BatchProcessor(analyzer)
        df_with_deps = processor.process_repositories(df)

        print("🔄 Transformando dependencias a columnas...")
        df_final = transform_dependencies_to_columns(df_with_deps)

        # Guardar datos
        data_manager.save_data(df_final)

        print("\n📊 Resumen final:")
        print(f"✅ Total repositorios procesados: {len(df_final)}")
        print(f"✅ Total dependencias únicas encontradas: {len([col for col in df_final.columns if col.startswith('dep_')])}")
        print(f"⚠️ Repositorios con errores: {len(df_final[df_final['dep_error'].notna()])}")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()
