from abc import ABC, abstractmethod

class PipelineStep(ABC):
    """
    Clase base abstracta para definir pasos en el pipeline.
    """

    def __init__(self, input_path, output_path, next_step=None):  # ✅ Se agrega next_step con un valor por defecto
        self.input_path = input_path
        self.output_path = output_path
        self.next_step = next_step  # ✅ Almacena la referencia al siguiente paso en la cadena

    @abstractmethod
    def process(self, df):
        """
        Método que debe implementarse en cada paso del pipeline.
        """
        pass
