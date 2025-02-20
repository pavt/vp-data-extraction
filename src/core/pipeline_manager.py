from src.core.pipeline_chain import PipelineStep
from src.utils.logger import logger
from src.core.data_manager import DataManager
from src.core.process_step import ProcessStep  # ✅ Nueva importación

class PipelineManager:
    """
    Clase para gestionar el pipeline de procesamiento de datos.
    """

    def __init__(self):
        self.data_paths = {
            "capa_0": "data/processed/datos_capa_0.csv",
            "capa_1": "data/processed/datos_capa_1.csv",
            "capa_2": "data/processed/datos_capa_2.csv",
        }

    def run(self):
        """
        Ejecuta el pipeline completo utilizando la cadena de procesamiento.
        """
        logger.info("🚀 Iniciando pipeline de procesamiento de repositorios...")

        df = self.load_data()
        pipeline = ProcessStep("capa_1", self.data_paths["capa_0"], self.data_paths["capa_1"],
            ProcessStep("capa_2", self.data_paths["capa_1"], self.data_paths["capa_2"])
        )
        
        df = pipeline.execute(df)
        logger.info(f"✅ Pipeline completado. Datos finales en {self.data_paths['capa_2']}")

    def load_data(self):
        """
        Capa 0: Cargar datos originales.
        """
        input_file = "data/raw/repositories_raw_data.csv"
        logger.info("📂 [Capa 0] Cargando datos originales...")
        data_manager = DataManager(input_file, self.data_paths["capa_0"])
        df = data_manager.load_data()
        data_manager.save_data(df)
        return df
