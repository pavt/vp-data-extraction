from abc import ABC, abstractmethod

class PipelineStep(ABC):
    """
    Clase base abstracta para definir pasos en el pipeline.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @abstractmethod
    def process(self, df):
        """
        Método que debe implementarse en cada paso del pipeline.
        """
        pass
