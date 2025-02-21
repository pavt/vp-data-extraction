import sys
import os

# 🔹 Asegurar que src/ está en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.core.pipeline_manager import PipelineManager  # ✅ Corrección

if __name__ == "__main__":
    pipeline = PipelineManager(
        raw_data_path="data/raw/repositories_raw_data_test.csv"  # ✅ Solo necesitamos el raw
    )
    pipeline.run()
