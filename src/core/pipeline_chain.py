from src.core.pipeline_step import PipelineStep

class PipelineChain:
    """
    Gestiona la ejecución secuencial de los pasos del pipeline.
    """

    def __init__(self):
        self.first_step = None
        self.last_step = None

    def add_step(self, step: PipelineStep):
        """
        Agrega un paso al pipeline y lo encadena correctamente.
        """
        if self.first_step is None:
            self.first_step = step
        else:
            self.last_step.next_step = step
        self.last_step = step

    def run(self, df):
        """
        Ejecuta el pipeline desde el primer paso.
        """
        if self.first_step:
            return self.first_step.execute(df)
        else:
            raise RuntimeError("No hay pasos en el pipeline.")
