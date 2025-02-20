from src.core.processor_factory import ProcessorFactory
from src.core.pipeline_chain import PipelineStep
from src.utils.logger import logger

class ProcessStep(PipelineStep):
    """
    Paso genérico que ejecuta una estrategia de procesamiento.
    """

    def __init__(self, capa, input_path, output_path, next_step=None):
        super().__init__(next_step)
        self.strategy = ProcessorFactory.get_processor(capa, input_path, output_path)

    def process(self, df):
        logger.info(f"⚙️ Ejecutando {self.strategy.__class__.__name__}...")
        return self.strategy.process(df)
