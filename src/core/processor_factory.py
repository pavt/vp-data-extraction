from src.processing.strategies.language_strategy import LanguageProcessingStrategy
from src.processing.strategies.dependency_strategy import DependencyProcessingStrategy

class ProcessorFactory:
    """
    Fábrica para instanciar estrategias de procesamiento según la capa.
    """

    @staticmethod
    def get_processor(capa, input_path, output_path):
        """
        Retorna la estrategia adecuada según la capa.
        """
        if capa == "capa_1":
            return LanguageProcessingStrategy(input_path, output_path)
        elif capa == "capa_2":
            return DependencyProcessingStrategy(input_path, output_path)
        else:
            raise ValueError(f"❌ Capa '{capa}' no reconocida en ProcessorFactory.")
