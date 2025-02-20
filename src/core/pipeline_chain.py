from abc import ABC, abstractmethod
from src.utils.logger import logger

class PipelineStep(ABC):
    """
    Clase base abstracta para definir pasos en el pipeline.
    """

    def __init__(self, next_step=None):
        self.next_step = next_step

    @abstractmethod
    def process(self, df):
        """
        Método que debe implementarse en cada paso del pipeline.
        """
        pass

    def execute(self, df):
        """
        Ejecuta el paso actual y, si hay un siguiente paso, lo ejecuta.
        """
        try:
            df = self.process(df)
            if self.next_step:
                return self.next_step.execute(df)
            return df
        except Exception as e:
            logger.error(f"❌ Error en {self.__class__.__name__}: {e}")
            return df  # Continúa con el pipeline aunque haya errores
