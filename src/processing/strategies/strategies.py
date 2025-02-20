from abc import ABC, abstractmethod

class ProcessingStrategy(ABC):
    """
    Clase base abstracta para definir estrategias de procesamiento.
    """

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @abstractmethod
    def process(self, df):
        """
        Método abstracto que debe ser implementado por cada estrategia de procesamiento.
        """
        pass
